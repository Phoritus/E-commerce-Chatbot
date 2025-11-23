from app.core.config import chroma_config
from chromadb import CloudClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from app.core.logging import logger

ef = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = None
collection = None
try:
    chroma_client = CloudClient(
        api_key=chroma_config.CHROMA_API_KEY,
        tenant=chroma_config.CHROMA_TENANT,
        database=chroma_config.database_name,
    )
    collection = chroma_client.get_or_create_collection(
        name="ecommerce_collection",
        embedding_function=ef,
    )
except Exception as e:
    logger.warning(f"ChromaDB not initialized: {e}. Proceeding without collection.")
  
