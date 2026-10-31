from app.ai_copilot.embedding_service import generate_embedding

text = "Machine M029 experienced unexpected downtime."

embedding = generate_embedding(text)

print("Embedding generated successfully")
print("Dimensions:", len(embedding))
print("First five values:", embedding[:5])