from app.services.router_search import check_route
from app.services.sql_query import SQLQueryService
from app.db.postgresdb import get_db
from app.services.chat_bot_service import ChatBotService
from app.services.small_talk import SmallTalkService
from app.models.chat_bot_model import ChatBotState, ChatBotRequest

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

# Determine the route based on the *latest* user message
def router_node(state: ChatBotState):
    # Get the last message (Human Message)
    last_message = state["messages"][-1]
    question = last_message.content
    print(f"Router checking question: {question}")
    
    route_name = check_route(question)
    return {"destination": route_name}

def route_decision(state: dict):
    return state["destination"]

# Node wrapper functions that conform to StateGraph signature
def faq_node(state: ChatBotState):
    question = state["messages"][-1].content
    history = state["messages"][:-1] # get history without current question
    chat_bot_service = ChatBotService()
    chat_bot_service.ingest_faq_data()
    # Pass history to service
    answer = chat_bot_service.get_faq_answer(question, history)
    return {"messages": [AIMessage(content=answer)]}

def product_inquiry_node(state: ChatBotState):
    question = state["messages"][-1].content
    history = state["messages"][:-1]
    with get_db() as db:
        sql_service = SQLQueryService(db=db)
        # We don't need to generate query separately here if sql_chain does it.
        # But if we want to print it for debugging, we can.
        # However, sql_chain generates it again internally. 
        # For efficiency, we should rely on sql_chain OR split it up. 
        # Given current sql_chain implementation, let's just call sql_chain with history.
        
        answer = sql_service.sql_chain(question, history)
        return {"messages": [AIMessage(content=answer)]}

def small_talk_node(state: ChatBotState):
    question = state["messages"][-1].content
    history = state["messages"][:-1]
    small_talk_service = SmallTalkService()
    # Pass history
    answer = small_talk_service.get_response(question, history)
    return {"messages": [AIMessage(content=answer)]}

def default_node(state: ChatBotState):
    return {"messages": [AIMessage(content="Sorry, I cannot handle this type of question yet.")]}

# Build the graph
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
        "default": "default"  # Assuming check_route might return something else or we can handle fallback
    }
)
builder.add_edge("faq", END)
builder.add_edge("product_inquiry", END)
builder.add_edge("small_talk", END)
builder.add_edge("default", END)

# Initialize Checkpointer
memory_checkpointer = MemorySaver()

# Compile the graph
graph = builder.compile(checkpointer=memory_checkpointer)

def chat_bot_route(request: ChatBotRequest):
    try:
        print(f"Processing request for thread_id: {request.thread_id}")
        
        # Prepare input state
        initial_state = {
            "messages": [HumanMessage(content=request.question)]
        }
        
        # Invoke graph with config for persistence
        config = {"configurable": {"thread_id": request.thread_id}}
        
        # Run!
        result = graph.invoke(initial_state, config=config)
        
        # Extract the final answer (last message)
        final_answer = result["messages"][-1].content
        return final_answer

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Error in chat_bot_route: {error_msg}")
        return f"An error occurred: {str(e)}"