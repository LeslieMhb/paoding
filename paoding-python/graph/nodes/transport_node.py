"""Transport consultation node."""

from langchain_core.messages import SystemMessage, HumanMessage

from config.settings import settings
from graph.types import ChatState
from graph.nodes.java_client import search_flights, search_trains


TRANSPORT_SYSTEM_PROMPT = """你是一个专业的交通出行助手。根据用户的出行需求，结合搜索结果为用户推荐合适的交通方式。

请用自然、友好的语气回复用户，包含以下信息：
1. 推荐的出行方式及理由
2. 航班/车次的关键信息（班次号、时间、价格、承运方）
3. 不同选择的优缺点对比

如果搜索结果为空，请礼貌地告知用户并建议调整搜索条件。"""


def _extract_transport_params(messages: list) -> dict:
    """Extract transport search parameters from conversation history."""
    last_msg = messages[-1].content if messages else ""

    params = {
        "dep_city": "杭州",
        "arr_city": "北京",
        "go_date": "2026-06-01",
    }

    city_keywords = {
        "北京": "北京", "上海": "上海", "杭州": "杭州", "成都": "成都",
        "广州": "广州", "深圳": "深圳", "南京": "南京", "西安": "西安",
        "重庆": "重庆", "厦门": "厦门", "苏州": "苏州", "大理": "大理",
        "三亚": "三亚", "丽江": "丽江",
    }

    found_cities = []
    for city_name, city_val in city_keywords.items():
        if city_name in last_msg:
            found_cities.append(city_val)

    if len(found_cities) >= 2:
        params["dep_city"] = found_cities[0]
        params["arr_city"] = found_cities[1]
    elif len(found_cities) == 1:
        params["arr_city"] = found_cities[0]

    return params


async def transport_consult_node(state: ChatState) -> dict:
    """Handle transport consultation with Java service data."""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0.7,
    )

    messages = state.get("messages", [])
    params = _extract_transport_params(messages)

    # Call Java service for both flights and trains
    try:
        flight_data = await search_flights(
            dep_city=params["dep_city"],
            arr_city=params["arr_city"],
            go_date=params["go_date"],
        )
    except Exception:
        flight_data = {"flightList": [], "recommendTitle": "航班搜索暂时不可用"}

    try:
        train_data = await search_trains(
            dep_city=params["dep_city"],
            arr_city=params["arr_city"],
            go_date=params["go_date"],
        )
    except Exception:
        train_data = {"trainList": [], "recommendTitle": "火车票搜索暂时不可用"}

    flight_summary = _format_flight_list(flight_data.get("flightList", []))
    train_summary = _format_train_list(train_data.get("trainList", []))

    context = f"""出发地：{params["dep_city"]} → 目的地：{params["arr_city"]} | 日期：{params["go_date"]}

航班信息：
{flight_summary}

火车票信息：
{train_summary}

请根据以上搜索结果回答用户的问题。"""

    full_messages = [
        SystemMessage(content=TRANSPORT_SYSTEM_PROMPT),
        HumanMessage(content=context),
    ] + list(messages[-3:])

    chunks = []
    async for chunk in llm.astream(full_messages):
        chunks.append(chunk.content)
    return {"response": "".join(chunks)}


def _format_flight_list(flight_list: list) -> str:
    """Format flight list for LLM context."""
    if not flight_list:
        return "暂无航班信息"

    lines = []
    for f in flight_list[:5]:
        no = f.get("transportNo", "未知")
        dep_time = f.get("departureTime", "")
        arr_time = f.get("arrivalTime", "")
        duration = f.get("timeInterval", "")
        dep_station = f.get("departureStation", "")
        arr_station = f.get("arrivalStation", "")
        carrier = f.get("carrier", "")
        price = f.get("totalPrice", 0)
        price_yuan = f"¥{price / 100:.0f}" if price else "价格未知"
        transfer = "（中转）" if f.get("transfer") else ""

        lines.append(
            f"- {no}{transfer} | {carrier}\n"
            f"  {dep_time}→{arr_time}（{duration}）\n"
            f"  {dep_station} → {arr_station}\n"
            f"  票价：{price_yuan}"
        )

    return "\n\n".join(lines)


def _format_train_list(train_list: list) -> str:
    """Format train list for LLM context."""
    if not train_list:
        return "暂无火车票信息"

    lines = []
    for t in train_list[:5]:
        no = t.get("transportNo", "未知")
        dep_time = t.get("departureTime", "")
        arr_time = t.get("arrivalTime", "")
        duration = t.get("timeInterval", "")
        dep_station = t.get("departureStation", "")
        arr_station = t.get("arrivalStation", "")
        train_type = t.get("trainType", "")
        seat = t.get("seatType", "")
        price = t.get("totalPrice", 0)
        price_yuan = f"¥{price / 100:.0f}" if price else "价格未知"

        lines.append(
            f"- {no}（{train_type}）| {seat}\n"
            f"  {dep_time}→{arr_time}（{duration}）\n"
            f"  {dep_station} → {arr_station}\n"
            f"  票价：{price_yuan}"
        )

    return "\n\n".join(lines)
