
from app.ai_copilot.retrieval_service import retrieve_relevant_chunks


questions = [
    "How is Overall Equipment Effectiveness calculated?",
    "What manufacturing data is available?",
    "What are the limitations of the manufacturing dataset?"
]

for question in questions:
    print("\n" + "=" * 70)
    print("QUESTION:", question)

    results = retrieve_relevant_chunks(question, top_k=3)

    for result in results:
        print("\nDocument:", result["document_name"])
        print("Chunk:", result["chunk_index"])
        print("Similarity:", round(float(result["similarity"]), 4))
        print("Content:", result["content"][:400])
