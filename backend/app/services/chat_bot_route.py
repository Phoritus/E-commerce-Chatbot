from app.services.router_search import check_route
from app.services.sql_query import SQLQueryService
from app.db.postgresdb import get_db
from app.services.chat_bot_service import ChatBotService
from app.services.small_talk import SmallTalkService

def chat_bot_route(user_question: str):
    try:
        print("User question:", user_question)
        route_name = check_route(user_question)
        if route_name == "faq":
            chat_bot_service = ChatBotService()
            chat_bot_service.ingest_faq_data()
            answer = chat_bot_service.get_faq_answer(user_question)
            return answer
        elif route_name == "product_inquiry":
            with get_db() as db:
                sql_service = SQLQueryService(db=db)
                # sql query command
                sql_query = sql_service.generate_sql_query(user_question)
                print(sql_query)
                
                answer = sql_service.sql_chain(user_question)
                return answer
        elif route_name == "small_talk":
            small_talk_service = SmallTalkService()
            answer = small_talk_service.get_response(user_question)
            return answer
        else:
            return "Sorry, I cannot handle this type of question yet."
    except Exception as e:
        return f"An error occurred: {str(e)}"