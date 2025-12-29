from typing import List, Literal
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.core.config import google_config
from app.db.postgresdb import get_db
from app.models.chat_bot_model import ChatBotState, ChatBotRequest, RouterDecision
from app.services.router_search import check_route
from app.services.sql_query import SQLQueryService
from app.services.chat_bot_service import ChatBotService
from app.services.small_talk import SmallTalkService

# 1. PRE-INITIALIZE MODELS & SERVICES (Optimal Way)
# Initialize models once globally to avoid overhead
BASE_LLM = init_chat_model(
    model="google_genai:gemini-2.0-flash",
    api_key=google_config.GOOGLE_API_KEY,
    temperature=0.2
)

# Initialize Services once (Ingest FAQ data once at startup, not per request)
FAQ_SERVICE = ChatBotService()
FAQ_SERVICE.ingest_faq_data() 
SMALL_TALK_SERVICE = SmallTalkService()

# Create the structured router LLM
ROUTER_LLM = BASE_LLM.with_structured_output(RouterDecision)

# 2. OPTIMIZED NODES

def router_node(state: ChatBotState):
    """Semantic Router first (Fast), LLM with History second (Smart)."""
    messages = state["messages"]
    last_message = messages[-1].content
    
    # Fast path: Semantic Router (No cost, high speed)
    route_name = check_route(last_message)
    
    # Fallback path: LLM with Context (Handles "Those/It/Cheapest")
    if route_name is None:
        print(f"--- Semantic Router ambiguous. Calling LLM Fallback ---")
        # Optimization: Pass history so LLM knows what "Those" refers to
        decision = ROUTER_LLM.invoke(messages)
        # Handle both dict and pydantic object return types
        route_name = decision.route if hasattr(decision, 'route') else decision["route"]
    
    print(f"--- Route Decision: {route_name} ---")
    return {"destination": route_name}

def route_decision(state: dict):
    return state["destination"]

def faq_node(state: ChatBotState):
    # History is already managed by state["messages"]
    answer = FAQ_SERVICE.get_faq_answer(
        state["messages"][-1].content, 
        state["messages"][:-1]
    )
    return {"messages": [AIMessage(content=answer)]}

def product_inquiry_node(state: ChatBotState):
    with get_db() as db:
        # Pass the pre-existing DB session
        sql_service = SQLQueryService(db=db)
        # sql_chain handles the SQL generation and summarization internally
        answer = sql_service.sql_chain(
            state["messages"][-1].content, 
            state["messages"][:-1]
        )
        return {"messages": [AIMessage(content=answer)]}

def small_talk_node(state: ChatBotState):
    answer = SMALL_TALK_SERVICE.get_response(
        state["messages"][-1].content, 
        state["messages"][:-1]
    )
    return {"messages": [AIMessage(content=answer)]}

def default_node(state: ChatBotState):
    return {"messages": [AIMessage(content="I'm sorry, I couldn't categorize your request. How can I help?")]}

# 3. GRAPH CONSTRUCTION

builder = StateGraph(ChatBotState)

builder.add_node("router", router_node)
builder.add_node("faq", faq_node)
builder.add_node("product_inquiry", product_inquiry_node)
builder.add_node("small_talk", small_talk_node)
builder.add_node("default", default_node)

builder.add_edge(START, "router")
builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "faq": "faq",
        "product_inquiry": "product_inquiry",
        "small_talk": "small_talk",
        "default": "default"
    }
)

builder.add_edge("faq", END)
builder.add_edge("product_inquiry", END)
builder.add_edge("small_talk", END)
builder.add_edge("default", END)

# Persistence
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 4. API ENTRY POINT

def chat_bot_route(request: ChatBotRequest):
    try:
        # thread_id ensures MemorySaver loads the correct history
        config = {"configurable": {"thread_id": request.thread_id}}
        
        # LangGraph automatically merges this HumanMessage with previous history in MemorySaver
        initial_state = {"messages": [HumanMessage(content=request.question)]}
        
        result = graph.invoke(initial_state, config=config)
        return result["messages"][-1].content

    except Exception as e:
        import traceback
        print(f"Error in chat_bot_route: {traceback.format_exc()}")
        return f"I encountered an error. Please try again or rephrase your question."