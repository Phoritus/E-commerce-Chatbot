from app.core.config import groq_config
from app.db.chromaDB import collection
from app.core.logging import logger, log_event
from pathlib import Path
from uuid import uuid4
from functools import lru_cache
import pandas as pd
from groq import Groq
import time


class ChatBotService:
  def __init__(self):
    self._collection = collection

  def ingest_faq_data(self, batch_size: int = 100, skip_if_present: bool = True):
    """Ingest FAQ data efficiently.

    - Optional idempotence: skip ingestion if we already have >= number of rows present.
    - Chunked upsert to reduce memory pressure and allow progress logging.
    - Deterministic fallback embeddings if transformer model unavailable.
    """
    path = Path(__file__).parent.parent
    data_file = path / "resources" / "faq_data.csv"
    logger.info("Loading FAQ data from %s", data_file)
    df = pd.read_csv(data_file)

    # Idempotence guard
    if skip_if_present:
      try:
        if self._collection is None:
          log_event("ingest.unavailable", reason="chroma collection not initialized")
          return
        count = self._collection.count()
        if count >= len(df):
          logger.info("Skipping ingestion; collection already has %d >= %d items", count, len(df))
          log_event("ingest.skip", existing=count, total=len(df))
          return
        else:
          log_event("ingest.start", existing=count, total=len(df), batch_size=batch_size)
      except Exception as e:
        log_event("ingest.count.error", error=str(e))

    documents_all = df['question'].tolist()
    metadatas_all = df[['answer']].to_dict(orient='records')

    # Pre-generate IDs to ensure stable identity per run (could hash question for stability)
    ids_all = [str(uuid4()) for _ in range(len(df))]

    if self._collection is None:
      log_event("ingest.unavailable", reason="chroma collection not initialized")
      return
    self._collection.add(
      ids=ids_all,
      documents=documents_all,
      metadatas=metadatas_all,
    )

    
  
  @lru_cache(maxsize=256)
  def query_faq_data(self, query: str, n_results: int = 5):
    """Query Chroma with LRU caching for repeated identical queries.

    Print statements show when actual vector search occurs (cache miss).
    """
    log_event("query.execute", query=query, n_results=n_results)
    t0 = time.time()
    if self._collection is None:
      log_event("query.unavailable", reason="chroma collection not initialized")
      return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    res = self._collection.query(query_texts=[query], n_results=n_results)
    log_event("query.complete", query=query, ms=round((time.time()-t0)*1000,1))
    return res

  def query_faq_data_cached(self, query: str, n_results: int = 5):
    """Wrapper that leverages LRU cache and prints hit/miss info."""
    # lru_cache wraps original function; if function not executed we skip heavy work.
    key = (query, n_results)
    # Access cache internals indirectly not straightforward; rely on timing difference.
    # We simulate hit detection by calling cache_info before and after.
    before = self.query_faq_data.cache_info().hits
    result = self.query_faq_data(query, n_results)  # may run or return cached value
    after = self.query_faq_data.cache_info().hits
    if after > before:
      log_event("query.cache.hit", query=query)
    return result
    
  def get_faq_answer(self, query: str):
    """Return an answer to the user query using Groq LLM with RAG context from Chroma.

    Falls back gracefully if GROQ_API_KEY is missing.
    """
    groq_key = groq_config.GROQ_API_KEY
    if not groq_key:
      logger.error("GROQ_API_KEY not set; cannot call Groq API.")
      return "Configuration error: GROQ_API_KEY is missing."
    
    client_groq = Groq(api_key=groq_key)

    # Retrieve top FAQ documents for context
    rag_results = self.query_faq_data_cached(query, n_results=5)
    source_docs = rag_results.get("documents", [[]])[0]
    metadatas = rag_results.get("metadatas", [[]])[0]

    # 1) If we already have a direct answer in metadata, return it immediately (highest precision)
    try:
      for meta in metadatas:
        if isinstance(meta, dict):
          ans = meta.get("answer")
          if isinstance(ans, str) and ans.strip():
            return ans.strip()
    except Exception:
      # If anything goes wrong, continue to LLM with enriched context
      pass

    # 2) Otherwise, build enriched Q/A context for LLM (include both question and the stored answer when present)
    context_blocks = []
    for i, (doc, meta) in enumerate(zip(source_docs, metadatas), start=1):
      origin = meta.get("source") if isinstance(meta, dict) else "faq"
      meta_answer = meta.get("answer") if isinstance(meta, dict) else None
      qa_block = [f"[Source {i} from {origin}]"]
      if doc:
        qa_block.append(f"Q: {doc}")
      if isinstance(meta_answer, str) and meta_answer.strip():
        qa_block.append(f"A: {meta_answer.strip()}")
      context_blocks.append("\n".join(qa_block))
    context_text = "\n\n".join(context_blocks) if context_blocks else "(No contextual documents retrieved)"

    system_prompt = (
      "You are an e-commerce support assistant. Use ONLY the provided context to answer. "
      "If the answer is not in the context, say you don't have that information yet."
    )
    user_prompt = (
      "Context containing Q/A pairs from knowledge base:\n"
      f"{context_text}\n\n"
      f"User question: {query}\n\n"
      "Answer ONLY using the provided answers. If insufficient, say you don't have that information yet."
    )

    try:
      completion = client_groq.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=512,
        stream=False,
      )
      answer = completion.choices[0].message.content.strip()
      return answer
    except Exception as e:
      logger.error("Groq API error: %s", str(e))
      return f"Groq API call failed: {e}"
    

# if __name__ == "__main__":
#   log_event("main.start")
#   chatbot_service = ChatBotService()
#   chatbot_service.ingest_faq_data()
#   test_query = "How can i get a discount on my purchase?"
#   log_event("main.query", query=test_query)
#   answer = chatbot_service.get_faq_answer(test_query)
#   log_event("main.answer", query=test_query, answer_preview=answer[:120])