import asyncio
import json
from typing import AsyncGenerator


async def run_agent_workflow(message: str, session_id: str, user_id: str) -> AsyncGenerator:
    """
    Main workflow entry point.
    TODO: Replace with actual LangGraph workflow execution.
    Currently yields mock SSE events for integration testing.
    """
    # Start thinking
    yield {"event": "start_thinking", "data": json.dumps({"session_id": session_id})}

    # Thinking process
    thinking_text = "正在分析您的问题..."
    for i, char in enumerate(thinking_text):
        yield {"event": "thinking", "data": json.dumps({"chunk": char})}
        await asyncio.sleep(0.03)

    yield {"event": "end_thinking", "data": json.dumps({})}

    # Start message
    yield {"event": "start_message", "data": json.dumps({"session_id": session_id})}

    # Stream message chunks
    response = f"您好！我收到了您的消息："{message}"。这是 MVP 版本的模拟回复，LangGraph 工作流尚未接入。"
    for char in response:
        yield {"event": "message", "data": json.dumps({"chunk": char})}
        await asyncio.sleep(0.02)

    # End message
    yield {"event": "end_message", "data": json.dumps({"session_id": session_id})}
