
import json

import ollama
from sqlalchemy import text

from app.database.connection import engine
from app.ai_copilot.embedding_service import generate_embedding
from app.ai_copilot.analytics_service import get_analytics_context


LLM_MODEL = "llama3.1"


def retrieve_documents(question: str, top_k: int = 3):
    """Retrieve relevant document chunks using pgvector."""

    embedding = generate_embedding(question)

    embedding_string = "[" + ",".join(
        str(value) for value in embedding
    ) + "]"

    with engine.connect() as connection:
        results = connection.execute(
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
                "embedding": embedding_string,
                "top_k": top_k
            }
        ).mappings().all()

    return [dict(row) for row in results]


def ask_manufacturing_question(
    question: str,
    top_k: int = 3
):
    """
    Hybrid Manufacturing AI Copilot.

    1. Retrieve manufacturing documentation.
    2. Retrieve PostgreSQL analytics.
    3. Retrieve anomaly and data-quality insights.
    4. Generate explanations and advisory recommendations.
    """

    # STEP 1: Retrieve relevant documentation
    documents = retrieve_documents(question, top_k)

    document_context = "\n\n".join(
        [
            f"""
Document: {doc['document_name']}
Chunk: {doc['chunk_index']}
Content: {doc['content']}
"""
            for doc in documents
        ]
    )

    # STEP 2: Retrieve manufacturing analytics
    analytics = get_analytics_context(question)

    analytics_context = json.dumps(
        analytics,
        indent=2,
        default=str
    )

    # STEP 3: Build the AI prompt
    prompt = f"""
You are an AI Manufacturing Analytics Copilot.

Use the supplied manufacturing documentation and database
analytics to answer the user's question.

DOCUMENTATION CONTEXT:
{document_context if document_context else "No relevant documentation found."}

MANUFACTURING DATABASE ANALYTICS:
{analytics_context}

CORE INSTRUCTIONS:

1. Use actual database values for numerical answers.
2. Use documentation to explain manufacturing concepts.
3. Never invent machine IDs, production counts, OEE values,
   downtime values or anomaly records.
4. Clearly distinguish database findings from recommendations.
5. Mention that OEE results are provisional when relevant.
6. Do not claim correlation or causation without evidence.
7. If information is unavailable, say so clearly.

ANOMALY EXPLANATION:

When anomaly information is available:

1. Identify the machine or observations present in the records.
2. Explain the unusual values using only available fields.
3. Explain why those observations may deserve investigation.
4. Do not interpret an anomaly as a confirmed equipment failure.

MAINTENANCE RECOMMENDATIONS:

Provide practical recommendations based on the available evidence.

Examples of advisory checks:

- For unusually high downtime:
  Review downtime event history and maintenance records.

- For unusually low production performance:
  Inspect operating speed, cycle time and production interruptions.

- For unusual quality measurements:
  Review inspection records, rejection patterns and process settings.

- For unusual machine behaviour:
  Review relevant operating conditions and maintenance history.

Only provide recommendations relevant to the actual available
data. Do not claim that a specific component is damaged or
requires replacement unless the evidence establishes that fact.

RECOMMENDATION FORMAT:

### Detected Observation
Explain what the analytics actually identified.

### Possible Operational Significance
Explain why the observation may matter.

### Recommended Checks
Provide practical checks for maintenance or production teams.

### Evidence and Limitations
Identify the available evidence and any missing information.

USER QUESTION:
{question}

Provide a clear, structured and evidence-based answer.
"""

    # STEP 4: Generate the answer using Ollama
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a manufacturing analytics expert. "
                    "Use only supplied documentation and analytics "
                    "as evidence. Recommendations must be advisory "
                    "and must not be presented as confirmed diagnoses."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False
    )

    answer = response["message"]["content"]

    # STEP 5: Prepare document sources
    sources = [
        {
            "document_name": doc["document_name"],
            "chunk_index": doc["chunk_index"],
            "similarity": round(
                float(doc["similarity"]), 4
            )
        }
        for doc in documents
    ]

    # STEP 6: Return the complete response
    safe_analytics = json.loads(
        json.dumps(analytics, default=str)
    )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "analytics": safe_analytics
    }
