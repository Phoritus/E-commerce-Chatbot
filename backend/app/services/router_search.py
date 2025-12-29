from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.routers import SemanticRouter


faq = Route(
  name="faq",
  utterances=[
    "What is the return policy of the products?",
    "How can I track my order?",
    "What payment methods are accepted?",
    "How do I contact customer support?",
    "Can I change or cancel my order?",
    "Are there any ongoing sales or promotions?",
    "What is the warranty on your products?",
    "How do I create an account?",
    "What are the shipping options available?",
    "How do I reset my password?",
    "How can I return a product I bought?",
  ]
)

small_talk = Route(
  name="small_talk",
  utterances=[
    "Hello",
    "Hi there",
    "How are you?",
    "What's up?",
    "Tell me a joke",
    "Goodbye",
    "See you later",
    "Thanks",
    "Thank you",
    "You're welcome",
    "How are you?",
    "What is your name?",
    "Are you a robot?",
    "What are you?",
    "What do you do?"
  ]
)

product_inquiry = Route(
    name="product_inquiry",
    utterances=[
      # Price & Discount (ถามราคาแบบระบุ Brand หรือ Category กว้างๆ)
      "How much are Nike shoes?",
      "Show me the price of mobile phones.",
      "Are there any discounts on shirts today?",
      "Find cheap running shoes.",
      "What is the price of Samsung mobile phones?",

      # Ratings & Reviews (ถามหาสินค้าดี/ยอดนิยม)
      "Which mobile phones have the best rating?",
      "Show me top rated shirts.",
      "Find shoes with 5 star ratings.",
      "Are Adidas shirts popular?",
      "Recommend mobile phones with good reviews.",
      "Which of those is the cheapest?",

      # Availability (ถามว่ามีของไหม โดยระบุยี่ห้อหรือประเภท)
      "Are Puma shoes in stock?",
      "Check if you have any mobile phones available.",
      "Do you have shirts in stock?",

      # Brand & Category (ค้นหาสินค้า)
      "I want to buy a mobile phone.",
      "Show me shirts from Nike.",
      "Do you sell shoes for running?",
      "List all available mobile phones.",

      # Link (ขอลิงก์ซื้อ)
      "Send me a link to buy shoes.",
      "Where can I order shirts?",
    ]
)


router = SemanticRouter(
    routes=[faq, product_inquiry, small_talk],
    encoder=HuggingFaceEncoder(
      name="sentence-transformers/all-mpnet-base-v2"
    ),
    auto_sync="local"
)

router.set_threshold(route_name="faq", threshold=0.25)
router.set_threshold(route_name="product_inquiry", threshold=0.25)
router.set_threshold(route_name="small_talk", threshold=0.25)


def check_route(user_query: str):
    matched_route = router(user_query)
    if matched_route is None:
        return None
    
    return matched_route.name

# if __name__ == "__main__":
#     test_questions = [
#         "How can I return a product?",
#         "Show me Nike shoes with discount",
#         "What is your name?",
#         "Do you have any mobile phones in stock?",
#         "Tell me a joke",
#         "Where can I buy Adidas shirts?"
#     ]

#     for question in test_questions:
#         route_name = check_route(question)
#         print(f"Question: {question}\nMatched Route: {route_name}\n")