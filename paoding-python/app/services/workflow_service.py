"""Workflow service - orchestrates LangGraph execution with real-time SSE streaming."""

import json
from typing import AsyncGenerator

from langchain_core.messages import HumanMessage, AIMessage

from graph.types import EventType, ChatState
from graph.builder import build_graph
from config.settings import settings

# Domain nodes that produce MESSAGE events (vs THINKING from reception)
_DOMAIN_NODES = {"hotel_consult", "transport_consult", "attraction_consult", "chatbot"}

_graph = None


def _get_graph():
    """Lazy-initialize the compiled graph."""
    global _graph
    if _graph is None:
        _graph = build_graph()
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
    graph = _get_graph()

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
    config = {"callbacks": [langfuse_handler]} if langfuse_handler else {}

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
