"""Reception node - classifies user intent and routes to appropriate node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage

from config.settings import settings
from graph.types import ChatState, IntentType


INTENT_CLASSIFICATION_PROMPT = """你是一个旅行助手的意图识别模块。根据用户的最新消息，判断用户的意图类别。

意图类别：
- hotel_consult: 用户想查询酒店、住宿、宾馆相关信息（如：找酒店、推荐住宿、酒店价格等）
- transport_consult: 用户想查询交通信息（如：机票、航班、火车票、高铁、出行方式等）
- attraction_consult: 用户想查询景点、旅游路线、行程规划（如：有什么好玩的、推荐景点、行程规划等）
- general_chat: 其他一般性对话（如：打招呼、闲聊、与旅行无关的问题等）

请只返回一个JSON对象，格式如下：
{"intent": "hotel_consult"}

只返回JSON，不要任何其他文字。"""


async def reception_node(state: ChatState) -> dict:
    """Classify user intent using LLM."""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )

    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None
    user_text = last_message.content if last_message else ""

    try:
        chunks = []
        async for chunk in llm.astream([
            SystemMessage(content=INTENT_CLASSIFICATION_PROMPT),
            HumanMessage(content=user_text),
        ]):
            chunks.append(chunk.content)
        full_response = "".join(chunks)

        result = json.loads(full_response.strip())
        intent = result.get("intent", IntentType.GENERAL_CHAT)

        # Validate intent
        valid_intents = [e.value for e in IntentType]
        if intent not in valid_intents:
            intent = IntentType.GENERAL_CHAT

    except (json.JSONDecodeError, KeyError, Exception):
        intent = IntentType.GENERAL_CHAT

    return {
        "current_intent": intent,
        "thinking": f"识别到用户意图：{intent}",
    }
