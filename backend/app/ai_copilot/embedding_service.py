
import ollama


EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:
    """
    Generate a 768-dimensional embedding using Ollama.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    embedding = response["embeddings"][0]

    if len(embedding) != 768:
        raise ValueError(
            f"Expected 768 dimensions, got {len(embedding)}"
        )

    return embedding
