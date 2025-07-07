import os
from dotenv import load_dotenv
from typing import List, Tuple, Any, Callable

import google.genai as genai
from google.genai import types
from google.genai.types import Content, Part
from langchain.schema import Document
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_community.vectorstores import FAISS
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
