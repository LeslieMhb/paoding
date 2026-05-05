from typing import Optional
from fastapi import APIRouter, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: str
    user_id: str
    history: Optional[list[ChatMessage]] = []


class CheckpointRequest(BaseModel):
    session_id: str
    checkpoint_id: str


@router.post("/sendMessage")
async def send_message(request: ChatRequest, req: Request):
    """SSE streaming chat endpoint."""
    from app.services.workflow_service import run_agent_workflow

    history = [(m.role, m.content) for m in (request.history or [])]
    return EventSourceResponse(
        run_agent_workflow(request.message, request.session_id, request.user_id, history),
        media_type="text/event-stream",
    )


@router.get("/checkpoints")
async def get_checkpoints(session_id: str):
    """List all checkpoints for a session (time travel history)."""
    from app.services.workflow_service import list_checkpoints

    checkpoints = await list_checkpoints(session_id)
    return {"session_id": session_id, "checkpoints": checkpoints}


@router.get("/checkpoints/{checkpoint_id}")
async def get_checkpoint_detail(session_id: str, checkpoint_id: str):
    """Get the state at a specific checkpoint."""
    from app.services.workflow_service import get_state_at_checkpoint

    state = await get_state_at_checkpoint(session_id, checkpoint_id)
    if state is None:
        return {"error": "Checkpoint not found"}
    return state


@router.post("/replay")
async def replay_checkpoint(request: CheckpointRequest, req: Request):
    """Replay (re-execute) the graph from a specific checkpoint (time travel)."""
    from app.services.workflow_service import replay_from_checkpoint

    return EventSourceResponse(
        replay_from_checkpoint(request.session_id, request.checkpoint_id),
        media_type="text/event-stream",
    )
