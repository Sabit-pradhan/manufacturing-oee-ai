
from pathlib import Path

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


def load_document(file_path: str) -> dict:
    """
    Extract text and metadata from PDF, DOCX, TXT, or Markdown files.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported document format: {extension}")

    # Extract text from PDF files.
    if extension == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )

    # Extract text from Word documents.
    elif extension == ".docx":
        document = Document(str(path))
        text = "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    # Read plain-text and Markdown files.
    else:
        text = path.read_text(encoding="utf-8")

    text = text.strip()

    if not text:
        raise ValueError(f"No readable text found in: {path.name}")

    return {
        "document_name": path.name,
        "document_type": extension.lstrip("."),
        "content": text,
        "character_count": len(text),
    }
