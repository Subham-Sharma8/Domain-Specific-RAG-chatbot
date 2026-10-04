from io import BytesIO
from typing import BinaryIO, Dict, List
from pypdf import PdfReader


def extract_pdf_pages(file_obj: BinaryIO, filename: str) -> List[Dict]:
    """Extract non-empty page text while preserving document and page metadata."""
    if not filename.lower().endswith(".pdf"):
        raise ValueError(f"{filename} is not a PDF file.")

    data = file_obj.read()
    max_bytes = 15 * 1024 * 1024
    if len(data) > max_bytes:
        raise ValueError(f"{filename} exceeds the 15 MB upload limit.")

    reader = PdfReader(BytesIO(data))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split()).strip()
        if not text:
            continue
        pages.append({
            "document": filename,
            "page": page_number,
            "text": text,
        })

    return pages
