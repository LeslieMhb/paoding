"""Java service HTTP client."""

import httpx
from config.settings import settings

_client = httpx.AsyncClient(timeout=30.0)


async def search_hotels(arr_city: str, from_date: str, to_date: str, **kwargs) -> dict:
    """Search hotels from Java service."""
    resp = await _client.post(
        f"{settings.java_service_url}/api/v1/hotel/search",
        json={"arrCity": arr_city, "fromDate": from_date, "toDate": to_date, **kwargs},
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"] if data.get("ret") else {}


async def get_hotel_detail(hotel_seq: str) -> dict:
    """Get hotel detail from Java service."""
    resp = await _client.get(
        f"{settings.java_service_url}/api/v1/hotel/detail/{hotel_seq}",
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"] if data.get("ret") else {}


async def search_flights(dep_city: str, arr_city: str, go_date: str, **kwargs) -> dict:
    """Search flights from Java service."""
    resp = await _client.post(
        f"{settings.java_service_url}/api/v1/transport/flight/search",
        json={"depCity": dep_city, "arrCity": arr_city, "goDate": go_date, **kwargs},
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"] if data.get("ret") else {}


async def search_trains(dep_city: str, arr_city: str, go_date: str, **kwargs) -> dict:
    """Search trains from Java service."""
    resp = await _client.post(
        f"{settings.java_service_url}/api/v1/transport/train/search",
        json={"depCity": dep_city, "arrCity": arr_city, "goDate": go_date, **kwargs},
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"] if data.get("ret") else {}


async def search_attractions(arrival: str, **kwargs) -> dict:
    """Search attractions from Java service."""
    resp = await _client.post(
        f"{settings.java_service_url}/api/v1/attraction/search",
        json={"arrival": arrival, **kwargs},
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"] if data.get("ret") else {}


async def plan_route(arrival: str, days: int, **kwargs) -> dict:
    """Plan route from Java service."""
    resp = await _client.post(
        f"{settings.java_service_url}/api/v1/attraction/route/plan",
        json={"arrival": arrival, "days": days, **kwargs},
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"] if data.get("ret") else {}
