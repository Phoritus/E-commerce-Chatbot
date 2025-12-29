from app.core.config import groq_config

from langchain_groq import ChatGroq
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage


class SQLQueryService:
    def __init__(self, db: Session):
        self._db = db
        self._client_groq = ChatGroq(
            api_key=groq_config.GROQ_API_KEY,
            model="openai/gpt-oss-20b",
            temperature=0.2,
            model_kwargs={"stream": False}
        )
        
        # PROMPT 1: SQL Generation (Context-Aware)
        self.sql_prompt = """
            You are a PostgreSQL expert. Generate a raw SQL query based on the user's question and Chat History.

            ### Schema:
            Table: public.amazon_product_data
            Columns: id, product_link, title, brand, discount, avg_rating, total_ratings, availability, category, price

            ### Strict Rules:
            1. **Output ONLY the SQL string.** Do NOT include markdown blocks (```sql), no backticks, and no text before/after the query.
            2. **Context Persistence:** If the user asks about "those" or "them", REUSE the category or filters from the previous message in the Chat History.
            - *Example:* If History shows "Show me shoes" and User asks "Which is cheapest?", your SQL must include `WHERE category ILIKE '%shoes%'`.
            3. **The "Cheapest" Logic:** When asked for the cheapest, always use `ORDER BY price ASC LIMIT 1`.
            4. **Text Search:** Use `ILIKE '%keyword%'` for titles and categories.
            5. **Selection:** You MUST always SELECT: `title`, `price`, `avg_rating`, `product_link`, and `discount`.
            6. **Avoid Over-Filtering:** Do not add filters that the user didn't ask for (like brand or rating) unless specified.
        """
        
        # PROMPT 2: Data Comprehension (Summarization)
        self.comprehension_prompt = """
            You are a friendly Shopping Assistant. Summarize the database results for the user.

            ### Currency & Formatting:
            - ALL prices provided are in Thai Baht (THB). 
            - You MUST display prices with the "THB" suffix (e.g., "450.00 THB"). 
            - NEVER use the "$" symbol.
            - Round all prices to 2 decimal places.

            ### Communication Guidelines:
            1. **Context Awareness:** If the user asked a follow-up question (like "Which of those..."), start your response by acknowledging the previous list.
            2. **Highlights:**List the top 1-3 most relevant items using bullet points or more than that if it necessary.
            3. **Link Format:** Always format links as `[**Title**](product_link)`.
            4. **Empty Results:** If the database results are empty, apologize and ask if they want to try a broader search.
            5.**Display Format:** If it need to show rating use start emoji (⭐) to show rating.
        """

    def generate_sql_query(self, user_question: str, history: list = []):
        """Generates a PostgreSQL query based on user input and conversation history."""
        messages = [SystemMessage(content=self.sql_prompt)]
        
        # Inject history so the LLM knows what was searched previously
        messages.extend(history) 
        messages.append(HumanMessage(content=user_question))
        
        response = self._client_groq.invoke(messages)
        return response.content.strip()

    def run_sql_query(self, sql_query: str):
        """Executes the generated SQL query and returns a Pandas DataFrame."""
        try:
            result = self._db.execute(text(sql_query))
            data = result.fetchall()
            return pd.DataFrame(data, columns=result.keys())
        except Exception as e:
            print(f"SQL Execution Error: {e}")
            return pd.DataFrame()

    def data_comprehension(self, user_question: str, data: pd.DataFrame, history: list = []):
        """Converts raw database rows into a natural language response."""
        data_list = data.to_dict(orient='records')[:10] # Limit to top 10 for context window
        
        messages = [SystemMessage(content=self.comprehension_prompt)]
        messages.extend(history) # Let the assistant remember what it said before
        
        context_query = f"User Question: {user_question}\nDatabase Results: {data_list}"
        messages.append(HumanMessage(content=context_query))
        
        response = self._client_groq.invoke(messages, temperature=0.3)
        return response.content

    def sql_chain(self, user_question: str, history: list = []):
        """Main entry point: Question -> SQL -> Data -> Answer."""
        # 1. Generate SQL (Looking at history to handle 'those/them')
        sql_query = self.generate_sql_query(user_question, history)
        
        # 2. Execute SQL
        result_df = self.run_sql_query(sql_query)
        
        if result_df.empty:
            return "I'm sorry, I couldn't find any products matching that request right now."

        # 3. Formulate Answer (Looking at history to stay consistent)
        answer = self.data_comprehension(user_question, result_df, history)
        return answer


# if __name__ == "__main__":
#     with get_db() as db:
#         test = SQLQueryService(db)
#         question = "Do you have shirts product in stock?"
#         sql_query = test.generate_sql_query(question)
#         print(sql_query)
#         # sql_query = """SELECT * FROM public.amazon_product_data ORDER BY id ASC"""
#         res = test.run_sql_query(sql_query)
#         print(res)
#         answer = test.data_comprehension(question, res)
#         print(answer)
