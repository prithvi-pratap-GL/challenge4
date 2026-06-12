"""PDF page rendering to images."""

import logging
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def render_pdf_pages(
    pdf_path: str,
    output_dir: Optional[str] = None,
    dpi: int = 150,
) -> list[str]:
    """Render PDF pages as images.

    Args:
        pdf_path: Path to PDF file.
        output_dir: Directory to save rendered images. Defaults to temp directory.
        dpi: DPI for rendering. Higher = better quality, slower. Defaults to 150.

    Returns:
        List of paths to rendered image files.

    Raises:
        FileNotFoundError: If PDF file doesn't exist.
        ValueError: If PDF is invalid or has no pages.
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if output_dir is None:
        output_dir = Path("/tmp/venturemind_renders")
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise ValueError(f"Failed to open PDF: {e}") from e

    if len(doc) == 0:
        raise ValueError("PDF has no pages")

    image_paths = []

    # Render each page at specified DPI
    zoom = dpi / 72  # 72 is default DPI in PDF

    for page_num in range(len(doc)):
        try:
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))

            # Save as PNG
            image_path = output_dir / f"page_{page_num + 1}.png"
            pix.save(str(image_path))
            image_paths.append(str(image_path))

            logger.debug(f"Rendered page {page_num + 1} to {image_path}")

        except Exception as e:
            logger.error(f"Failed to render page {page_num + 1}: {e}")
            raise

    doc.close()

    logger.info(f"Rendered {len(image_paths)} pages from {pdf_path}")
    return image_paths
