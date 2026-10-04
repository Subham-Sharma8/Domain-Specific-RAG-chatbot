from pathlib import Path
from document_loader import extract_pdf_pages
from langchain_text_splitters import RecursiveCharacterTextSplitter


def test_sample_pdf_exists():
    pdfs = list(Path("documents").glob("*.pdf"))
    assert len(pdfs) >= 1


def test_pdf_extraction():
    pdf = next(Path("documents").glob("*.pdf"))
    with open(pdf, "rb") as f:
        pages = extract_pdf_pages(f, pdf.name)
    assert pages
    assert all("document" in p and "page" in p and "text" in p for p in pages)


def test_chunking():
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split_text("This is a test document. " * 30)
    assert len(chunks) > 1
