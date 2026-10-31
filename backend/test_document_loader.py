
from pathlib import Path

from app.ai_copilot.document_loader import load_document


PROJECT_ROOT = Path(__file__).resolve().parents[1]

documents = [
    PROJECT_ROOT / "data" / "docs" / "DATA_DICTIONARY.md",
    PROJECT_ROOT / "data" / "raw" / "realtime_manufacturing_dataset" / "README.md",
]

for file_path in documents:
    result = load_document(str(file_path))

    print("Document:", result["document_name"])
    print("Type:", result["document_type"])
    print("Characters:", result["character_count"])
    print("Preview:", result["content"][:300])
