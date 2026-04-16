from fastapi import APIRouter
from schemas.models import ChatRequest, ChatResponse
from agents.orchestrator import run_agent

router = APIRouter()

@router.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    state = await run_agent(req.message)
    return ChatResponse(
        answer=state.get("query_result") or "I'm not sure how to help with that.",
        chart=state.get("chart_json"),
        notification=state.get("notification"),
        intent=state.get("intent", "general")
    )
