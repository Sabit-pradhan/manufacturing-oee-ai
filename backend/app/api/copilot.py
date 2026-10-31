
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai_copilot.rag_service import ask_manufacturing_question

router = APIRouter(
    prefix="/api/v1/copilot",
    tags=["Manufacturing AI Copilot"]
)


class CopilotRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000
    )
    top_k: int = Field(default=3, ge=1, le=10)


@router.post("/ask")
def ask_copilot(request: CopilotRequest):
    try:
        result = ask_manufacturing_question(
            question=request.question,
            top_k=request.top_k
        )
        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Copilot processing failed: {str(exc)}"
        )
