"""LangGraph workflow builder."""

from typing import Optional

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from graph.types import ChatState, IntentType
from graph.nodes.reception import reception_node
from graph.nodes.hotel_node import hotel_consult_node
from graph.nodes.transport_node import transport_consult_node
from graph.nodes.attraction_node import attraction_consult_node
from graph.nodes.chatbot_node import chatbot_node


def route_intent(state: ChatState) -> str:
    """Route to appropriate node based on classified intent."""
    intent = state.get("current_intent", IntentType.GENERAL_CHAT)

    routing = {
        IntentType.HOTEL_CONSULT: "hotel_consult",
        IntentType.TRANSPORT_CONSULT: "transport_consult",
        IntentType.ATTRACTION_CONSULT: "attraction_consult",
        IntentType.GENERAL_CHAT: "chatbot",
    }

    return routing.get(intent, "chatbot")


def build_graph(checkpointer: Optional[BaseCheckpointSaver] = None) -> CompiledStateGraph:
    """Build and compile the agent workflow graph.

    Args:
        checkpointer: Optional checkpoint saver for state persistence and time travel.
    """
    graph = StateGraph(ChatState)

    # Add nodes
    graph.add_node("reception", reception_node)
    graph.add_node("hotel_consult", hotel_consult_node)
    graph.add_node("transport_consult", transport_consult_node)
    graph.add_node("attraction_consult", attraction_consult_node)
    graph.add_node("chatbot", chatbot_node)

    # Set entry point
    graph.set_entry_point("reception")

    # Add conditional edges from reception
    graph.add_conditional_edges(
        "reception",
        route_intent,
        {
            "hotel_consult": "hotel_consult",
            "transport_consult": "transport_consult",
            "attraction_consult": "attraction_consult",
            "chatbot": "chatbot",
        },
    )

    # All domain nodes go to END
    graph.add_edge("hotel_consult", END)
    graph.add_edge("transport_consult", END)
    graph.add_edge("attraction_consult", END)
    graph.add_edge("chatbot", END)

    compiled = graph.compile(checkpointer=checkpointer)
    print(compiled.get_graph().draw_mermaid())
    return compiled
