from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.intent_classifier import classify_intent
from agents.data_query_agent import run_data_query
from agents.analysis_agent import run_deep_analysis
from agents.visualization_agent import run_visualization
from agents.report_agent import run_report
from agents.notification_agent import check_notification

class AgentState(TypedDict):
    user_message: str
    history: list[dict]
    intent: str
    requires_notification: bool
    region_mentioned: Optional[str]
    query_result: str
    chart_json: Optional[dict]
    report: Optional[str]
    notification: Optional[dict]
    error: Optional[str]

def _get_history(state: AgentState) -> str:
    hist = state.get("history", [])
    if not hist:
        return "No previous context."
    return "\n".join([f"{msg.get('role', 'unknown').capitalize()}: {msg.get('content', '')}" for msg in hist])

def intent_classifier_node(state: AgentState):
    classification = classify_intent(state["user_message"], _get_history(state))
    return {
        "intent": classification.get("intent", "general"),
        "requires_notification": classification.get("requires_notification", False),
        "region_mentioned": classification.get("region_mentioned")
    }

def data_query_node(state: AgentState):
    answer = run_data_query(state["user_message"], _get_history(state))
    return {"query_result": answer}

def deep_analysis_node(state: AgentState):
    answer = run_deep_analysis(state["user_message"], _get_history(state))
    return {"query_result": answer}

def visualization_node(state: AgentState):
    chart = run_visualization(state["user_message"], _get_history(state))
    msg = "I've generated the graph." if chart else "Failed to build visualization."
    return {"chart_json": chart, "query_result": msg}

def report_node(state: AgentState):
    report_data = run_report(state["user_message"], _get_history(state))
    return {
        "report": report_data.get("markdown_report"),
        "query_result": report_data.get("bot_message", "Report compiled successfully.")
    }

def notification_check_node(state: AgentState):
    if state.get("requires_notification") and state.get("region_mentioned"):
        notif = check_notification(state["region_mentioned"])
        if notif:
            return {"notification": notif}
    return {}

def general_reply_node(state: AgentState):
    return {"query_result": "Hello! I am your S&OP AI agent. I can help with data querying and visualizations regarding sales and operations."}

def build_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("intent_classifier", intent_classifier_node)
    graph.add_node("data_query", data_query_node)
    graph.add_node("deep_analysis", deep_analysis_node)
    graph.add_node("visualization", visualization_node)
    graph.add_node("report", report_node)
    graph.add_node("notification_check", notification_check_node)
    graph.add_node("general_reply", general_reply_node)
    
    graph.set_entry_point("intent_classifier")
    
    def route_intent(state: AgentState) -> str:
        intent = state.get("intent")
        if intent == "data_query":
            return "data_query"
        elif intent == "deep_analysis":
            return "deep_analysis"
        elif intent == "visualization":
            return "visualization"
        elif intent == "report":
            return "report"
        else:
            return "general_reply"
            
    graph.add_conditional_edges("intent_classifier", route_intent, {
        "data_query": "data_query",
        "deep_analysis": "deep_analysis",
        "visualization": "visualization",
        "report": "report",
        "general_reply": "general_reply"
    })
    
    graph.add_edge("data_query", "notification_check")
    graph.add_edge("deep_analysis", "notification_check")
    graph.add_edge("visualization", "notification_check")
    graph.add_edge("report", "notification_check")
    graph.add_edge("general_reply", END)
    graph.add_edge("notification_check", END)
    
    return graph.compile()

# Singleton graph build
agent_graph = build_graph()

async def run_agent(user_message: str, history: list[dict] = []) -> dict:
    state = await agent_graph.ainvoke({"user_message": user_message, "history": history})
    return state
