import os
import logging
import re
import uuid
import asyncio
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Import your existing embedding provider
from backend.infrastructure.embeddings.provider import EmbeddingProvider

# ---> ADD THIS IMPORT FOR THE VISION MODEL <---
from backend.infrastructure.parsers.vision_parser import VisionPdfParser

logger = logging.getLogger("ventuermind.ingestion")
router = APIRouter(prefix="/api/v1", tags=["ingestion"])

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Real Clients
qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant_api_key = os.getenv("QDRANT_API_KEY", "")
qdrant_client = AsyncQdrantClient(url=qdrant_url, api_key=qdrant_api_key)

embedder = EmbeddingProvider()
COLLECTION_NAME = "startup_website_chunks"
# Instantiate the vision parser
vision_parser = VisionPdfParser()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value)
    value = value.strip("-")
    return value or uuid.uuid4().hex[:8]


def derive_deal_id(pitch_deck: Optional[UploadFile], company_url: Optional[str]) -> str:
    if company_url:
        domain = re.sub(r"^https?://", "", company_url.strip())
        domain = domain.split("/")[0].replace("www.", "")
        return slugify(domain.split(".")[0])
    if pitch_deck and pitch_deck.filename:
        return slugify(Path(pitch_deck.filename).stem)
    return slugify(uuid.uuid4().hex[:8])


async def ensure_qdrant_collection():
    """Automatically creates the missing Qdrant table and enforces indexes."""
    try:
        exists = await qdrant_client.collection_exists(COLLECTION_NAME)
        if not exists:
            logger.info(f"Creating missing Qdrant collection: {COLLECTION_NAME}")
            await qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            
        await qdrant_client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="deal_id",
            field_schema="keyword",
        )
    except Exception as e:
        logger.error(f"Error checking/creating collection: {e}")


@router.post("/ingest")
async def ingest_deal(
    pitch_deck: Optional[UploadFile] = File(None),
    company_url: Optional[str] = Form(None),
):
    if not pitch_deck and not company_url:
        raise HTTPException(status_code=400, detail="Provide at least a pitch deck or URL.")

    deal_id = derive_deal_id(pitch_deck, company_url)
    logger.info(f"[ingestion:{deal_id}] Starting LIVE ingestion pipeline")

    chunks = []
    pdf_filename = None

    # 1. PROCESS PDF
    if pitch_deck:
        pdf_filename = f"{deal_id}_{pitch_deck.filename}"
        save_path = UPLOAD_DIR / pdf_filename
        contents = await pitch_deck.read()
        with open(save_path, "wb") as f:
            f.write(contents)

        logger.info(f"[STEP 1] PDF SAVED: {save_path}")
        doc = fitz.open(save_path)
        logger.info(f"[STEP 2] OPENING PDF: {save_path} ({len(doc)} pages)")

        vision_tasks = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().strip()
            
            # ---> THE FIX: Force Vision Model if text is less than 5000 characters <---
            if len(text) < 5000:
                logger.info(f"[STEP 2] Page {page_num+1} lacks text. Triggering Vision Model.")
                # Render the image for the vision model
                pix = page.get_pixmap(dpi=150)
                temp_img_path = f"temp_page_{page_num+1}.png"
                pix.save(temp_img_path)
                
                # Queue the vision task
                task = vision_parser.parse_page(image_path=temp_img_path, raw_text=text)
                vision_tasks.append((page_num + 1, task, temp_img_path))
            else:
                # Use standard text extraction if it actually has text
                for para in text.split('\n\n'):
                    clean_para = para.strip()
                    if len(clean_para) > 40:
                        chunks.append({"text": clean_para, "source_id": f"deck_p{page_num+1}"})

        # ---> Await all Vision tasks concurrently <---
        if vision_tasks:
            logger.info(f"[STEP 2] Awaiting {len(vision_tasks)} concurrent Vision API calls...")
            for p_num, task, img_path in vision_tasks:
                try:
                    analysis = await task
                    # Format the visual response into a dense chunk
                    combined_text = (
                        f"Visual Summary: {analysis.visual_summary}\n"
                        f"Claims: {', '.join(analysis.claims)}\n"
                        f"Metrics: {', '.join(analysis.metrics)}"
                    )
                    chunks.append({"text": combined_text, "source_id": f"deck_p{p_num}_vision"})
                except Exception as e:
                    logger.error(f"[STEP 2] Vision API failed on page {p_num}: {e}")
                finally:
                    # Clean up temp images
                    if os.path.exists(img_path):
                        os.remove(img_path)

        logger.info(f"[STEP 2] PDF extraction complete. Total chunks from PDF: {len(chunks)}")

    # 2. PROCESS WEBSITE (Keep existing logic)
    if company_url:
        logger.info(f"[ingestion:{deal_id}] Crawling URL: {company_url}")
        try:
            resp = requests.get(company_url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
                clean_text = element.get_text(separator=' ', strip=True)
                if len(clean_text) > 40:
                    # Check if it's the Akamai Error block
                    if "errors.edgesuite.net" not in clean_text:
                        chunks.append({"text": clean_text, "source_id": "website_crawl"})
        except Exception as e:
            logger.error(f"[ingestion:{deal_id}] Web crawl failed: {e}")

    if not chunks:
        raise HTTPException(status_code=400, detail="Could not extract usable text.")

    logger.info(f"[STEP 3] CHUNKING COMPLETE: {len(chunks)} chunks created")

    # 3. DATABASE SETUP & UPSERT
    await ensure_qdrant_collection()

    points = []
    for idx, chunk in enumerate(chunks):
        vector = embedder.embed(chunk["text"])
        points.append(PointStruct(
            id=uuid.uuid4().hex,
            vector=vector,
            payload={
                "deal_id": deal_id,
                "source_id": chunk["source_id"],
                "text": chunk["text"],
                "category": "uncategorized"
            }
        ))

    logger.info(f"[STEP 5] QDRANT UPSERT: Collection='{COLLECTION_NAME}', Points={len(points)}")

    batch_size = 50
    total_upserted = 0
    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        await qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
        total_upserted += len(batch)
        logger.info(f"[STEP 5] Batch upserted: {total_upserted}/{len(points)}")

    response_data = {
        "success": True,
        "deal_id": deal_id,
        "chunks_processed": len(points),
    }

    if pdf_filename:
        response_data["pdf_url"] = f"/uploads/{pdf_filename}"

    return JSONResponse(status_code=200, content=response_data)