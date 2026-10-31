
from sqlalchemy import text

from app.database.connection import SessionLocal
from app.ai_copilot.embedding_service import generate_embedding


def retrieve_relevant_chunks(
    query: str,
    top_k: int = 3
) -> list[dict]:
    """
    Find the most relevant document chunks using cosine similarity.
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # Convert the user's question into a 768-dimensional vector.
    query_embedding = generate_embedding(query)

    db = SessionLocal()

    try:
        result = db.execute(
            text("""
                SELECT
                    id,
                    document_name,
                    document_type,
                    chunk_index,
                    content,
                    1 - (embedding <=> CAST(:embedding AS vector))
                        AS similarity
                FROM document_chunks
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :top_k
            """),
            {
                "embedding": str(query_embedding),
                "top_k": top_k
            }
        )

        return [dict(row) for row in result.mappings().all()]

    finally:
        db.close()
