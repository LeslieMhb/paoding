"""General chatbot node for non-travel queries."""

from langchain_core.messages import SystemMessage

from config.settings import settings
from graph.types import ChatState


CHATBOT_SYSTEM_PROMPT = """你是"庖丁"，一个友好、专业的旅行助手。你可以帮助用户解答旅行相关的问题，也可以进行日常闲聊。

当用户询问旅行相关但意图不明确时，你可以：
1. 主动询问具体需求（目的地、时间、预算等）
2. 提供一些旅行建议和灵感
3. 引导用户使用酒店查询、交通查询、景点推荐等功能

请用自然、简洁的语气回复，避免过长的回答。"""


async def chatbot_node(state: ChatState) -> dict:
    """Handle general chat using LLM."""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0.7,
    )

    messages = state.get("messages", [])
    full_messages = [SystemMessage(content=CHATBOT_SYSTEM_PROMPT)] + list(messages[-5:])

    response = await llm.ainvoke(full_messages)

    return {"response": response.content}
