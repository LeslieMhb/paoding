"""Attraction consultation node."""

from langchain_core.messages import SystemMessage, HumanMessage

from config.settings import settings
from graph.types import ChatState
from graph.nodes.java_client import search_attractions, plan_route


ATTRACTION_SYSTEM_PROMPT = """你是一个专业的旅游景点推荐助手。根据用户的旅游需求，结合搜索结果为用户推荐合适的景点和行程。

请用自然、友好的语气回复用户，包含以下信息：
1. 推荐的景点及理由
2. 景点的关键信息（名称、类型、简介、贴士）
3. 如果有行程规划，给出每日安排建议

如果搜索结果为空，请礼貌地告知用户并建议调整搜索条件。"""


def _extract_attraction_params(messages: list) -> dict:
    """Extract attraction search parameters from conversation history."""
    last_msg = messages[-1].content if messages else ""

    params = {
        "arrival": "杭州",
        "days": 3,
    }

    city_keywords = {
        "北京": "北京", "上海": "上海", "杭州": "杭州", "成都": "成都",
        "广州": "广州", "深圳": "深圳", "南京": "南京", "西安": "西安",
        "重庆": "重庆", "厦门": "厦门", "苏州": "苏州", "大理": "大理",
        "三亚": "三亚", "丽江": "丽江",
    }
    for city_name, city_val in city_keywords.items():
        if city_name in last_msg:
            params["arrival"] = city_val
            break

    # Extract days
    import re
    day_match = re.search(r"(\d+)\s*[天日]", last_msg)
    if day_match:
        params["days"] = int(day_match.group(1))

    return params


async def attraction_consult_node(state: ChatState) -> dict:
    """Handle attraction consultation with Java service data."""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0.7,
    )

    messages = state.get("messages", [])
    params = _extract_attraction_params(messages)

    # Call Java service
    try:
        attraction_data = await search_attractions(arrival=params["arrival"])
    except Exception:
        attraction_data = {"attractionList": [], "recommendTitle": "景点搜索暂时不可用"}

    try:
        route_data = await plan_route(arrival=params["arrival"], days=params["days"])
    except Exception:
        route_data = {"dayRouteList": [], "title": "行程规划暂时不可用"}

    attraction_summary = _format_attraction_list(attraction_data.get("attractionList", []))
    route_summary = _format_route(route_data)

    context = f"""目的地：{params["arrival"]}

景点推荐：
{attraction_summary}

行程规划：
{route_summary}

请根据以上搜索结果回答用户的问题。"""

    full_messages = [
        SystemMessage(content=ATTRACTION_SYSTEM_PROMPT),
        HumanMessage(content=context),
    ] + list(messages[-3:])

    chunks = []
    async for chunk in llm.astream(full_messages):
        chunks.append(chunk.content)
    return {"response": "".join(chunks)}


def _format_attraction_list(attraction_list: list) -> str:
    """Format attraction list for LLM context."""
    if not attraction_list:
        return "暂无景点信息"

    lines = []
    for a in attraction_list[:5]:
        name = a.get("title", "未知")
        detail = a.get("detail", {})
        subtitle = detail.get("subtitle", "")
        desc = detail.get("description", "")
        tips = detail.get("tips", [])

        tips_text = "；".join(tips) if tips else ""
        lines.append(
            f"- {name}（{subtitle}）\n"
            f"  简介：{desc}\n"
            f"  贴士：{tips_text}"
        )

    return "\n\n".join(lines)


def _format_route(route_data: dict) -> str:
    """Format route plan for LLM context."""
    title = route_data.get("title", "")
    day_routes = route_data.get("dayRouteList", [])

    if not day_routes:
        return "暂无行程规划"

    lines = [f"路线：{title}"]
    for d in day_routes:
        day = d.get("day", "")
        theme = d.get("theme", "")
        route_text = d.get("routeText", "")
        highlights = d.get("highlights", "")
        full_desc = d.get("fullDesc", "")

        lines.append(
            f"\n第{day}天：{theme}\n"
            f"  路线：{route_text}\n"
            f"  亮点：{highlights}\n"
            f"  详细：{full_desc}"
        )

    return "\n".join(lines)
