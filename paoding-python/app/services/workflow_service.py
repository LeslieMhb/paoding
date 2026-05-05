"""Workflow service - orchestrates LangGraph execution with real-time SSE streaming."""

import json
from typing import AsyncGenerator

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from graph.types import EventType, ChatState
from graph.builder import build_graph
from config.settings import settings

# Domain nodes that produce MESSAGE events (vs THINKING from reception)
_DOMAIN_NODES = {"hotel_consult", "transport_consult", "attraction_consult", "chatbot"}

_graph = None
_checkpointer: AsyncSqliteSaver | None = None
_checkpointer_cm = None


async def init_checkpointer():
    """Initialize the async SQLite checkpointer (call during app startup)."""
    global _checkpointer, _checkpointer_cm
    if _checkpointer is None:
        _checkpointer_cm = AsyncSqliteSaver.from_conn_string("checkpoints.db")
        _checkpointer = await _checkpointer_cm.__aenter__()
        await _checkpointer.setup()


async def close_checkpointer():
    """Close the checkpointer (call during app shutdown)."""
    global _checkpointer, _checkpointer_cm
    if _checkpointer_cm:
        await _checkpointer_cm.__aexit__(None, None, None)
        _checkpointer = None
        _checkpointer_cm = None


def get_checkpointer() -> AsyncSqliteSaver | None:
    """Return the initialized checkpointer (None if not yet initialized)."""
    return _checkpointer


async def _get_graph():
    """Lazy-initialize the compiled graph with checkpointer."""
    global _graph
    if _graph is None:
        _graph = build_graph(checkpointer=_checkpointer)
    return _graph


def _setup_langfuse(session_id: str, user_id: str):
    """Set up Langfuse tracing context with propagated trace attributes.

    Uses propagate_attributes() to set trace-level session_id, user_id, and
    a descriptive trace_name. The CallbackHandler created inside this context
    auto-inherits the trace context per Langfuse best practices.

    Returns (context_manager, handler) or (None, None) if disabled/unavailable.
    """
    if not settings.langfuse_enabled:
        return None, None
    try:
        from langfuse import propagate_attributes
        from langfuse.langchain import CallbackHandler

        cm = propagate_attributes(
            trace_name="paoding-chat",
            session_id=session_id,
            user_id=user_id,
        )
        cm.__enter__()
        handler = CallbackHandler()
        return cm, handler
    except Exception:
        return None, None


def _teardown_langfuse(cm, handler):
    """Tear down Langfuse tracing context and flush pending traces."""
    if cm:
        try:
            cm.__exit__(None, None, None)
        except Exception:
            pass
    if handler:
        try:
            from langfuse import get_client
            get_client().flush()
        except Exception:
            pass


async def run_agent_workflow(
    message: str, session_id: str, user_id: str, history: list[tuple[str, str]] | None = None
) -> AsyncGenerator:
    """
    Main workflow entry point.
    Executes LangGraph workflow via astream_events and yields SSE events in real time.
    """
    graph = await _get_graph()

    # Build messages from history + current message
    messages = []
    if history:
        for role, content in history[-10:]:
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
    messages.append(HumanMessage(content=message))

    initial_state: ChatState = {
        "messages": messages,
        "session_id": session_id,
        "user_id": user_id,
        "current_intent": "",
        "current_message": message,
        "response": "",
        "thinking": "",
        "error": "",
    }

    # Set up Langfuse tracing with propagated attributes for session_id/user_id
    langfuse_cm, langfuse_handler = _setup_langfuse(session_id, user_id)
    config = {
        "configurable": {"thread_id": session_id},
    }
    if langfuse_handler:
        config["callbacks"] = [langfuse_handler]

    thinking_started = False
    message_started = False

    try:
        event_stream = graph.astream_events(initial_state, version="v2", config=config)

        async for event in event_stream:
            kind = event.get("event")
            name = event.get("name", "")
            metadata = event.get("metadata", {})
            langgraph_node = metadata.get("langgraph_node", "")

            # --- Reception node: thinking phase ---

            if langgraph_node == "reception":
                if kind == "on_chat_model_stream":
                    if not thinking_started:
                        thinking_started = True
                        yield {"event": EventType.START_THINKING, "data": json.dumps({"session_id": session_id})}

                    chunk_content = event.get("data", {}).get("chunk")
                    if chunk_content and chunk_content.content:
                        yield {"event": EventType.THINKING, "data": json.dumps({"chunk": chunk_content.content})}

                elif kind == "on_chain_end" and name == "reception":
                    if thinking_started:
                        yield {"event": EventType.END_THINKING, "data": json.dumps({})}

            # --- Domain nodes: message phase ---

            elif langgraph_node in _DOMAIN_NODES:
                if kind == "on_chat_model_stream":
                    if not message_started:
                        message_started = True
                        yield {"event": EventType.START_MESSAGE, "data": json.dumps({"session_id": session_id})}

                    chunk_content = event.get("data", {}).get("chunk")
                    if chunk_content and chunk_content.content:
                        yield {"event": EventType.MESSAGE, "data": json.dumps({"chunk": chunk_content.content})}

                elif kind == "on_chain_end" and name in _DOMAIN_NODES:
                    if message_started:
                        message_started = False
                        yield {"event": EventType.END_MESSAGE, "data": json.dumps({"session_id": session_id})}

    except Exception as e:
        if thinking_started:
            yield {"event": EventType.END_THINKING, "data": json.dumps({})}
        if message_started:
            yield {"event": EventType.END_MESSAGE, "data": json.dumps({"session_id": session_id})}
        yield {"event": EventType.ERROR, "data": json.dumps({"error": str(e)})}

    finally:
        _teardown_langfuse(langfuse_cm, langfuse_handler)

    yield {"event": EventType.CONVERSATION_ENDING, "data": json.dumps({})}


async def list_checkpoints(session_id: str) -> list[dict]:
    """List all checkpoints for a given session (thread).

    Returns a list of checkpoint metadata ordered from newest to oldest.
    Each checkpoint includes: checkpoint_id, node, timestamp, parent_checkpoint_id.
    """
    checkpointer = get_checkpointer()
    config = {"configurable": {"thread_id": session_id}}
    checkpoints = []
    async for state in checkpointer.alist(config):
        checkpoints.append({
            "checkpoint_id": state.config["configurable"]["checkpoint_id"],
            "node": state.metadata.get("source", ""),
            "timestamp": state.metadata.get("created_at", ""),
            "parent_checkpoint_id": state.parent_config.get("configurable", {}).get("checkpoint_id", "") if state.parent_config else "",
        })
    return checkpoints


async def get_state_at_checkpoint(session_id: str, checkpoint_id: str) -> dict | None:
    """Get the graph state at a specific checkpoint.

    Returns the full state dict at that checkpoint, or None if not found.
    """
    graph = await _get_graph()
    config = {"configurable": {"thread_id": session_id, "checkpoint_id": checkpoint_id}}
    snapshot = await graph.aget_state(config)
    if snapshot is None or snapshot.values is None:
        return None
    return {
        "checkpoint_id": checkpoint_id,
        "values": {k: v for k, v in snapshot.values.items() if k != "messages"},
        "messages": [
            {"role": msg.type, "content": msg.content}
            for msg in snapshot.values.get("messages", [])
        ],
        "next": list(snapshot.next),
    }


async def replay_from_checkpoint(session_id: str, checkpoint_id: str) -> AsyncGenerator:
    """Replay (re-execute) the graph from a specific checkpoint.

    This is the 'time travel' feature — restores state to the checkpoint,
    then re-runs the graph forward from that point.
    """
    graph = await _get_graph()
    config = {"configurable": {"thread_id": session_id, "checkpoint_id": checkpoint_id}}

    langfuse_cm, langfuse_handler = _setup_langfuse(session_id, "")
    if langfuse_handler:
        config["callbacks"] = [langfuse_handler]

    thinking_started = False
    message_started = False

    try:
        # None input means "resume from checkpoint state"
        event_stream = graph.astream_events(None, version="v2", config=config)

        async for event in event_stream:
            kind = event.get("event")
            name = event.get("name", "")
            metadata = event.get("metadata", {})
            langgraph_node = metadata.get("langgraph_node", "")

            if langgraph_node == "reception":
                if kind == "on_chat_model_stream":
                    if not thinking_started:
                        thinking_started = True
                        yield {"event": EventType.START_THINKING, "data": json.dumps({"session_id": session_id})}
                    chunk_content = event.get("data", {}).get("chunk")
                    if chunk_content and chunk_content.content:
                        yield {"event": EventType.THINKING, "data": json.dumps({"chunk": chunk_content.content})}
                elif kind == "on_chain_end" and name == "reception":
                    if thinking_started:
                        yield {"event": EventType.END_THINKING, "data": json.dumps({})}

            elif langgraph_node in _DOMAIN_NODES:
                if kind == "on_chat_model_stream":
                    if not message_started:
                        message_started = True
                        yield {"event": EventType.START_MESSAGE, "data": json.dumps({"session_id": session_id})}
                    chunk_content = event.get("data", {}).get("chunk")
                    if chunk_content and chunk_content.content:
                        yield {"event": EventType.MESSAGE, "data": json.dumps({"chunk": chunk_content.content})}
                elif kind == "on_chain_end" and name in _DOMAIN_NODES:
                    if message_started:
                        message_started = False
                        yield {"event": EventType.END_MESSAGE, "data": json.dumps({"session_id": session_id})}

    except Exception as e:
        if thinking_started:
            yield {"event": EventType.END_THINKING, "data": json.dumps({})}
        if message_started:
            yield {"event": EventType.END_MESSAGE, "data": json.dumps({"session_id": session_id})}
        yield {"event": EventType.ERROR, "data": json.dumps({"error": str(e)})}
    finally:
        _teardown_langfuse(langfuse_cm, langfuse_handler)

    yield {"event": EventType.CONVERSATION_ENDING, "data": json.dumps({})}
