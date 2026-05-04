"""LangGraph state type definitions."""

from enum import Enum
from typing import Annotated, Any

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class EventType(str, Enum):
    """SSE event types, aligned with libai-master."""
    HUMAN_MESSAGE = "human_message"
    START_THINKING = "start_thinking"
    THINKING = "thinking"
    END_THINKING = "end_thinking"
    START_MESSAGE = "start_message"
    MESSAGE = "message"
    END_MESSAGE = "end_message"
    ERROR = "error"
    CONVERSATION_ENDING = "conversation_ending"


class IntentType(str, Enum):
    """User intent classification."""
    HOTEL_CONSULT = "hotel_consult"
    TRANSPORT_CONSULT = "transport_consult"
    ATTRACTION_CONSULT = "attraction_consult"
    GENERAL_CHAT = "general_chat"


class ChatState(TypedDict, total=False):
    """Main graph state."""
    messages: Annotated[list[Any], add_messages]
    session_id: str
    user_id: str
    current_intent: str
    current_message: str
    response: str
    thinking: str
    error: str


class HotelState(TypedDict, total=False):
    """Hotel consultation sub-state."""
    query: dict
    results: list[dict]
    recommendation: str


class TransportState(TypedDict, total=False):
    """Transport consultation sub-state."""
    query: dict
    flight_results: list[dict]
    train_results: list[dict]
    recommendation: str


class AttractionState(TypedDict, total=False):
    """Attraction consultation sub-state."""
    query: dict
    results: list[dict]
    recommendation: str
