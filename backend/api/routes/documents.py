from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/api/v1/documents/{deal_id}")
async def get_document(deal_id: str):
    # Assuming your PDFs are stored in a folder named 'data/uploads'
    file_path = f"data/uploads/{deal_id}.pdf"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Document not found"}