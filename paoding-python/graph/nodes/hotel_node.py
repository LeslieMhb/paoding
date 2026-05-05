"""Hotel consultation node."""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from config.settings import settings
from graph.types import ChatState
from graph.nodes.java_client import search_hotels


HOTEL_SYSTEM_PROMPT = """你是一个专业的酒店咨询助手。根据用户的酒店查询需求，结合搜索结果为用户推荐合适的酒店。

请用自然、友好的语气回复用户，包含以下信息：
1. 推荐理由
2. 酒店的关键信息（名称、评分、价格、位置、特色）
3. 对比不同酒店的优缺点

如果搜索结果为空，请礼貌地告知用户并建议调整搜索条件。"""


def _extract_hotel_params(messages: list) -> dict:
    """Extract hotel search parameters from conversation history using simple heuristics."""
    last_msg = messages[-1].content if messages else ""

    params = {
        "arr_city": "杭州",
        "from_date": "2026-06-01",
        "to_date": "2026-06-03",
    }

    # Simple keyword extraction
    city_keywords = {
        "北京": "北京", "上海": "上海", "杭州": "杭州", "成都": "成都",
        "广州": "广州", "深圳": "深圳", "南京": "南京", "西安": "西安",
        "重庆": "重庆", "厦门": "厦门", "苏州": "苏州", "大理": "大理",
        "三亚": "三亚", "丽江": "丽江",
    }
    for city_name, city_val in city_keywords.items():
        if city_name in last_msg:
            params["arr_city"] = city_val
            break

    return params


async def hotel_consult_node(state: ChatState) -> dict:
    """Handle hotel consultation with Java service data."""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0.7,
    )

    messages = state.get("messages", [])
    params = _extract_hotel_params(messages)

    # Call Java service
    try:
        hotel_data = await search_hotels(
            arr_city=params["arr_city"],
            from_date=params["from_date"],
            to_date=params["to_date"],
        )
    except Exception as e:
        hotel_data = {"hotelList": [], "recommendTitle": "搜索暂时不可用"}

    # Build context for LLM
    hotel_list = hotel_data.get("hotelList", [])
    hotel_summary = _format_hotel_list(hotel_list)
    recommend_title = hotel_data.get("recommendTitle", "")

    context = f"""搜索结果：{recommend_title}

{hotel_summary}

请根据以上搜索结果回答用户的问题。"""

    full_messages = [
        SystemMessage(content=HOTEL_SYSTEM_PROMPT),
        HumanMessage(content=context),
    ] + list(messages[-3:])  # Include recent conversation for context

    chunks = []
    async for chunk in llm.astream(full_messages):
        chunks.append(chunk.content)
    return {"response": "".join(chunks)}


def _format_hotel_list(hotel_list: list) -> str:
    """Format hotel list for LLM context."""
    if not hotel_list:
        return "暂无搜索结果"

    lines = []
    for h in hotel_list[:5]:
        name = h.get("hotelName", "未知")
        score = h.get("score", "N/A")
        price_info = h.get("price", {})
        price_desc = price_info.get("priceDesc", "价格未知")
        addr = h.get("hotelAddress", "")
        location = h.get("locationInfo", "")
        dangci = h.get("dangciText", "")
        desc = h.get("hotelBriefDesc", "")
        tags = ", ".join(h.get("tagList", []))
        rec = h.get("recommendation", "")

        lines.append(
            f"- {name}（{dangci}）| 评分：{score} | 价格：{price_desc}\n"
            f"  地址：{addr} | 位置：{location}\n"
            f"  简介：{desc}\n"
            f"  标签：{tags}\n"
            f"  推荐语：{rec}"
        )

    return "\n\n".join(lines)
