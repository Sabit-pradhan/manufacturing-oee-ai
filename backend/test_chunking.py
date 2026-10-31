
from pathlib import Path

from app.ai_copilot.document_loader import load_document
from app.ai_copilot.chunking_service import chunk_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

file_path = (
    PROJECT_ROOT
    / "data"
    / "docs"
    / "DATA_DICTIONARY.md"
)

document = load_document(str(file_path))

chunks = chunk_text(document["content"])

print("Document:", document["document_name"])
print("Total characters:", document["character_count"])
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {index}:")
    print(chunk[:250])
