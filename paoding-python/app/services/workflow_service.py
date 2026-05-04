"""Workflow service - orchestrates LangGraph execution with SSE streaming."""

import json
import asyncio
from typing import AsyncGenerator

from langchain_core.messages import HumanMessage

from graph.types import EventType, ChatState
from graph.builder import build_graph


_graph = None


def _get_graph():
    """Lazy-initialize the compiled graph."""
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


async def run_agent_workflow(message: str, session_id: str, user_id: str) -> AsyncGenerator:
    """
    Main workflow entry point.
    Executes LangGraph workflow and yields SSE events for streaming.
    """
    graph = _get_graph()

    # Start thinking
    yield {"event": EventType.START_THINKING, "data": json.dumps({"session_id": session_id})}

    # Thinking phase
    thinking_text = "正在分析您的问题..."
    for char in thinking_text:
        yield {"event": EventType.THINKING, "data": json.dumps({"chunk": char})}
        await asyncio.sleep(0.02)

    # Execute graph
    try:
        initial_state: ChatState = {
            "messages": [HumanMessage(content=message)],
            "session_id": session_id,
            "user_id": user_id,
            "current_intent": "",
            "current_message": message,
            "response": "",
            "thinking": "",
            "error": "",
        }

        result = await graph.ainvoke(initial_state)

        # Update thinking with intent info
        thinking_result = result.get("thinking", "")
        if thinking_result:
            for char in thinking_result:
                yield {"event": EventType.THINKING, "data": json.dumps({"chunk": char})}
                await asyncio.sleep(0.01)

    except Exception as e:
        yield {"event": EventType.END_THINKING, "data": json.dumps({})}
        yield {"event": EventType.ERROR, "data": json.dumps({"error": str(e)})}
        yield {"event": EventType.CONVERSATION_ENDING, "data": json.dumps({})}
        return

    yield {"event": EventType.END_THINKING, "data": json.dumps({})}

    # Start message
    yield {"event": EventType.START_MESSAGE, "data": json.dumps({"session_id": session_id})}

    # Stream response character by character
    response = result.get("response", "抱歉，我暂时无法回答您的问题，请稍后再试。")
    for char in response:
        yield {"event": EventType.MESSAGE, "data": json.dumps({"chunk": char})}
        await asyncio.sleep(0.02)

    # End message
    yield {"event": EventType.END_MESSAGE, "data": json.dumps({"session_id": session_id})}

    # Conversation ending
    yield {"event": EventType.CONVERSATION_ENDING, "data": json.dumps({})}
