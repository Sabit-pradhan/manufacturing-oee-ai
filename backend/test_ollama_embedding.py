
import ollama

response = ollama.embed(
    model="nomic-embed-text",
    input="Manufacturing machine maintenance and downtime analysis"
)

embedding = response["embeddings"][0]

print("Model: nomic-embed-text")
print("Embedding dimensions:", len(embedding))
print("Sample values:", embedding[:5])
