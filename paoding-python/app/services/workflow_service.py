"""Workflow service - orchestrates LangGraph execution with real-time SSE streaming."""

import json
from typing import AsyncGenerator

from langchain_core.messages import HumanMessage, AIMessage

from graph.types import EventType, ChatState
from graph.builder import build_graph

# Domain nodes that produce MESSAGE events (vs THINKING from reception)
_DOMAIN_NODES = {"hotel_consult", "transport_consult", "attraction_consult", "chatbot"}

_graph = None


def _get_graph():
    """Lazy-initialize the compiled graph."""
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


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

    try:
        event_stream = graph.astream_events(initial_state, version="v2")

        thinking_started = False
        message_started = False

        async for event in event_stream:
            kind = event.get("event")
            name = event.get("name", "")
            metadata = event.get("metadata", {})
            langgraph_node = metadata.get("langgraph_node", "")

            # --- Reception node: thinking phase ---

            if langgraph_node == "reception":
                # Stream LLM tokens from reception as THINKING events
                if kind == "on_chat_model_stream":
                    if not thinking_started:
                        thinking_started = True
                        yield {"event": EventType.START_THINKING, "data": json.dumps({"session_id": session_id})}

                    chunk_content = event.get("data", {}).get("chunk")
                    if chunk_content and chunk_content.content:
                        yield {"event": EventType.THINKING, "data": json.dumps({"chunk": chunk_content.content})}

                # Reception chain ended
                elif kind == "on_chain_end" and name == "reception":
                    if thinking_started:
                        yield {"event": EventType.END_THINKING, "data": json.dumps({})}

            # --- Domain nodes: message phase ---

            elif langgraph_node in _DOMAIN_NODES:
                # Stream LLM tokens from domain nodes as MESSAGE events
                if kind == "on_chat_model_stream":
                    if not message_started:
                        message_started = True
                        yield {"event": EventType.START_MESSAGE, "data": json.dumps({"session_id": session_id})}

                    chunk_content = event.get("data", {}).get("chunk")
                    if chunk_content and chunk_content.content:
                        yield {"event": EventType.MESSAGE, "data": json.dumps({"chunk": chunk_content.content})}

                # Domain chain ended
                elif kind == "on_chain_end" and name in _DOMAIN_NODES:
                    if message_started:
                        message_started = False
                        yield {"event": EventType.END_MESSAGE, "data": json.dumps({"session_id": session_id})}

    except Exception as e:
        # Ensure we close any open phases on error
        if thinking_started:
            yield {"event": EventType.END_THINKING, "data": json.dumps({})}
        if message_started:
            yield {"event": EventType.END_MESSAGE, "data": json.dumps({"session_id": session_id})}
        yield {"event": EventType.ERROR, "data": json.dumps({"error": str(e)})}

    yield {"event": EventType.CONVERSATION_ENDING, "data": json.dumps({})}
