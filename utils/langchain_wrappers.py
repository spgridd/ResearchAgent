import os
from dotenv import load_dotenv

import google.genai as genai
from google.genai import types
from google.genai.types import Content, Part
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from sentence_transformers import CrossEncoder
import torch

from utils.client import get_client

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
CLIENT = get_client()


# Embbedding wrapper
class VertexAIEmbedding(Embeddings):
    def __init__(self, client: genai.Client = CLIENT, model: str = "models/text-embedding-004"):
        self.client = client
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [
            self._embed_text(text)
            for text in texts
        ]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)

    def _embed_text(self, text: str) -> list[float]:
        contents = Content(parts=[Part(text=text)])
        response = self.client.models.embed_content(
            model=f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/text-embedding-004",
            contents=contents,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
        )
        return response.embeddings[0].values
    

class CrossEncoderReRanker(BaseRetriever):
    retriever: BaseRetriever
    model: CrossEncoder
    top_n: int

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun):
        initial_docs = self.retriever.get_relevant_documents(query, callbacks=run_manager.get_child())
        
        if not initial_docs:
            return []
        
        doc_pairs = [[query, doc.page_content] for doc in initial_docs]

        with torch.no_grad():
            scores = self.model.predict(doc_pairs)
        
        docs_with_scores = list(zip(initial_docs, scores))
        sorted_docs_with_scores = sorted(docs_with_scores, key=lambda x: x[1], reverse=True)
        
        reranked_docs = [doc for doc, score in sorted_docs_with_scores[:self.top_n]]
        
        return reranked_docs