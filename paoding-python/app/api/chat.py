from fastapi import APIRouter, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str
    user_id: str


@router.post("/sendMessage")
async def send_message(request: ChatRequest, req: Request):
    """SSE streaming chat endpoint."""
    from app.services.workflow_service import run_agent_workflow

    return EventSourceResponse(
        run_agent_workflow(request.message, request.session_id, request.user_id),
        media_type="text/event-stream",
    )
