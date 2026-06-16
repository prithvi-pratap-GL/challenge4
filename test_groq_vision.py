#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Groq Vision Model Integration
"""
import asyncio
import sys
import os
import tempfile
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fitz
from backend.infrastructure.parsers.vision_parser import VisionPdfParser
from backend.core.settings import settings

async def test_groq_vision():
    """Test vision parser with Groq model."""

    tesla_pdf = "storage/uploads/tesla_tesla-pitch-deck.pdf"

    if not os.path.exists(tesla_pdf):
        print("[ERROR] Tesla PDF not found")
        return False

    print("[SETUP] Initializing VisionPdfParser with Groq")
    print("        API Key: {}...".format(settings.groq_api_key[:20]))
    print("        Base URL: {}".format(settings.groq_base_url))
    print("        Model: {}".format(settings.vision_model))
    print()

    parser = VisionPdfParser()

    print("[TEST] Opening Tesla PDF")
    doc = fitz.open(tesla_pdf)
    page = doc[0]
    raw_text = page.get_text("text")

    print("       Pages: {}".format(len(doc)))
    print("       Page 0 text length: {} chars".format(len(raw_text)))
    print()

    with tempfile.TemporaryDirectory() as temp_dir:
        image_path = os.path.join(temp_dir, "page_0.png")
        pix = page.get_pixmap(dpi=150)
        pix.save(image_path)
        print("[OK] Rendered page to PNG")
        print()

        print("[VISION TEST] Calling Groq vision model")
        print("              Model: {}".format(settings.vision_model))
        print()

        try:
            analysis = await parser.parse_page(image_path, raw_text)

            print("[SUCCESS] Vision analysis completed!")
            print()
            print("[RESULT] PageAnalysis:")
            print("  page_number: {}".format(analysis.page_number))
            print("  page_type: {}".format(analysis.page_type))
            print("  visual_summary: {}...".format(analysis.visual_summary[:100]))
            print("  claims: {} items".format(len(analysis.claims)))
            print("  metrics: {} items".format(len(analysis.metrics)))
            print("  entities: {} items".format(len(analysis.entities)))
            print()
            return True

        except Exception as e:
            print("[ERROR] Vision analysis failed:")
            print("        {}".format(str(e)))
            print()
            return False

    doc.close()

if __name__ == "__main__":
    result = asyncio.run(test_groq_vision())
    if result:
        print("[CONCLUSION] Groq vision model is OPERATIONAL!")
    else:
        print("[CONCLUSION] Groq vision model test FAILED")
    sys.exit(0 if result else 1)
