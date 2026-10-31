
from pathlib import Path

from app.ai_copilot.document_ingestion_service import ingest_document


PROJECT_ROOT = Path(__file__).resolve().parents[1]

document_path = (
    PROJECT_ROOT
    / "data"
    / "docs"
    / "DATA_DICTIONARY.md"
)

result = ingest_document(str(document_path))

print("\nDocument ingestion result:")
print(result)
