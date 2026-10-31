
from app.ai_copilot.rag_service import (
    ask_manufacturing_question
)


questions = [
    "How is OEE calculated in this manufacturing project?",

    "What is the scale of the manufacturing dataset?",

    "What are the important limitations of this dataset?"
]


for question in questions:

    print("\n" + "=" * 80)
    print("QUESTION:", question)

    result = ask_manufacturing_question(question)

    print("\nAI ANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(source)
