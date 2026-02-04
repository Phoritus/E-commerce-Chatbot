from app.core.config import chroma_config, google_config
from chromadb import CloudClient
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
from app.core.logging import logger

# Use Google's embedding API - no local model loading, much lighter on memory
ef = GoogleGenerativeAiEmbeddingFunction(
    api_key=google_config.GOOGLE_API_KEY,
    model_name="models/text-embedding-004"
)

chroma_client = None
collection = None
try:
    chroma_client = CloudClient(
        api_key=chroma_config.CHROMA_API_KEY,
        tenant=chroma_config.CHROMA_TENANT,
        database=chroma_config.database_name,
    )
    # New collection with Google embeddings (v2)
    collection = chroma_client.get_or_create_collection(
        name="ecommerce_collection_v2",
        embedding_function=ef,
    )
except Exception as e:
    logger.warning(f"ChromaDB not initialized: {e}. Proceeding without collection.")
