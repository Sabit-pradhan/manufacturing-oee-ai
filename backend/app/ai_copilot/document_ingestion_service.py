
from sqlalchemy import text

from app.database.connection import SessionLocal
from app.ai_copilot.document_loader import load_document
from app.ai_copilot.chunking_service import chunk_text
from app.ai_copilot.embedding_service import generate_embedding


def ingest_document(file_path: str) -> dict:
    """
    Load a document, split it into chunks, generate embeddings,
    and store them in PostgreSQL using pgvector.
    """

    document = load_document(file_path)

    chunks = chunk_text(
        document["content"],
        chunk_size=1000,
        overlap=150
    )

    if not chunks:
        raise ValueError("No chunks generated from document")

    db = SessionLocal()

    try:
        stored_count = 0

        for index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)

            db.execute(
                text("""
                    INSERT INTO document_chunks (
                        document_name,
                        document_type,
                        chunk_index,
                        content,
                        embedding,
                        metadata
                    )
                    VALUES (
                        :document_name,
                        :document_type,
                        :chunk_index,
                        :content,
                        CAST(:embedding AS vector),
                        CAST(:metadata AS jsonb)
                    )
                """),
                {
                    "document_name": document["document_name"],
                    "document_type": document["document_type"],
                    "chunk_index": index,
                    "content": chunk,
                    "embedding": str(embedding),
                    "metadata": '{"source": "local_document"}'
                }
            )

            stored_count += 1

        db.commit()

        return {
            "document_name": document["document_name"],
            "total_chunks": len(chunks),
            "stored_chunks": stored_count,
            "status": "success"
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
