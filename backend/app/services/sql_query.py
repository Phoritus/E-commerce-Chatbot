from app.core.config import groq_config
from app.db.postgresdb import dbSession

from groq import Groq
from sqlalchemy import text
import pandas as pd


class SQLQueryService:
    def __init__(self, db: dbSession):
        self._db = db
        self._client_groq = Groq(
            api_key=groq_config.GROQ_API_KEY,          
        )
        
        self.sql_prompt = """
            You are an expert PostgreSQL Database Administrator and Data Analyst.
            Your task is to generate accurate and efficient PostgreSQL queries based on natural language requests.

            ### Database Schema
            Table Name: public.amazon_product_data

            Columns:
            - id (BIGINT, PRIMARY KEY): Unique identifier for the product.
            - product_link (TEXT): URL link to the product.
            - title (TEXT): Name/Title of the product.
            - brand (TEXT): Brand name.
            - discount (DOUBLE PRECISION): Discount percentage (e.g., 0.15 for 15%).
            - avg_rating (DOUBLE PRECISION): Average customer rating (0-5).
            - total_ratings (INTEGER): Number of ratings.
            - availability (TEXT): Stock status description (e.g., 'In Stock', or NULL).
            - category (TEXT): Product category.
            - price (DOUBLE PRECISION): Product price in THB.

            ### Guidelines
            1. **Dialect:** Use standard PostgreSQL syntax.
            2. **Text Search:** Use `ILIKE` for case-insensitive string matching.
            3. **Null Handling:** Use `IS NOT NULL` or `COALESCE` where appropriate.
            4. **Mandatory Columns:** For any query that retrieves product rows, **YOU MUST ALWAYS INCLUDE** `product_link`, `discount`, `price` and `avg_rating` in the `SELECT` clause, along with other requested columns.
            5. **Optimization:** Always include `LIMIT 100` unless aggregation is requested.
            6. **Output Format (CRITICAL):** - Return **ONLY** the raw SQL query.
               - **DO NOT** use markdown backticks (```sql or ```).
               - **DO NOT** output JSON.
               - **DO NOT** add any explanation or conversational text.
               - The output must be ready to execute directly in a `db.execute()` function.

            ### Examples

            User: "ขอสินค้าที่มี rating มากกว่า 4.5 และราคาไม่เกิน 1000 บาท"
            Assistant: SELECT title, price, avg_rating, total_ratings, product_link, discount FROM public.amazon_product_data WHERE avg_rating > 4.5 AND price <= 1000 ORDER BY avg_rating DESC LIMIT 100;

            User: "นับจำนวนสินค้าแยกตามหมวดหมู่"
            Assistant: SELECT category, COUNT(*) AS product_count FROM public.amazon_product_data WHERE availability IS NOT NULL GROUP BY category ORDER BY product_count DESC;
        """
       
        self.comprehension_prompt = """
            You are a friendly and knowledgeable Personal Shopping Assistant (English Language).
            You will receive the **TOP 5** matching products from a larger database search.
            Your goal is to present these top picks naturally and summarize the options.

            ### Data Format Explanation:
            The data is a list of top-ranked products containing: 'title', 'price' (THB), 'avg_rating', 'total_ratings', 'brand', and optionally 'product_link'.

            ### Critical Rules for Links:
            - **IF 'product_link' exists:** Format as `[**Title**](URL)`.
            - **IF 'product_link' is missing:** Format as `**Title**`.

            ### Response Guidelines (Summary Style):
            1. **Tone:** Conversational, warm, and concise. Avoid listing data fields robotically.
            2. **The Highlight:** select the 3 most interesting items to display as bullet points.
            - Format: "- [Link/Title] - [Price] THB (⭐ [Rating])"
            3. **Price Overview:** Briefly mention the price range (e.g., "Prices for these start around 1,200 THB...").
            4. **Closing:** Ask if they want to see more details or specific brands.

            ### Example Scenario:
            User: "Show me running shoes"
            Data: [List of 5 shoe objects...]
            
            **Response:** "I found some excellent running shoes for you! Here are the top picks from our collection:
            
            - [**Nike Air Zoom Pegasus**](https://...): 4,200 THB (⭐ 4.8)
            - [**Adidas Ultraboost Light**](https://...): 6,500 THB (⭐ 4.7)
            - **New Balance Fresh Foam**: 3,200 THB (⭐ 4.5)
            
            Prices range from roughly 3,000 to 6,500 THB depending on the model. Would you like to narrow it down by budget?"
        """
        
    def generate_sql_query(self, user_question: str):
        response = self._client_groq.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": self.sql_prompt,
                },
                {
                    "role": "user",
                    "content": user_question,
                }
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    
        
    def run_sql_query(self, sql_query: str):
        result = self._db.execute(text(sql_query))
        data = result.fetchall()
        df = pd.DataFrame(data, columns=result.keys())
        return df
    
    def data_comprehension(self, user_question: str, data: pd.DataFrame):
        data_list = data.to_dict(orient='records')
        # cut off size if too large
        if (len(data_list) >= 100):
            data_list = data_list[:10]
        
        response = self._client_groq.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": self.comprehension_prompt,
                },
                {
                    "role": "user",
                    "content": f"User Question: {user_question}\nDatabase Results: {data_list}",
                }
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    
    def sql_chain(self, user_question: str):
        sql_query = self.generate_sql_query(user_question)
        result_df = self.run_sql_query(sql_query)
        answer = self.data_comprehension(user_question, result_df)
        return answer
    
    
        

# if __name__ == "__main__":
#     test = SQLQueryService(db=next(get_db()))
#     question = "Do you have shirts product in stock?"
#     sql_query = test.generate_sql_query(question)
#     print(sql_query)
    
#     res = test.run_sql_query(sql_query)
#     print(res)
    
#     answer = test.data_comprehension(question, res)
#     print(answer)
