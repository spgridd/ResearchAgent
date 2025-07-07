from dotenv import load_dotenv
import pickle
from langchain_community.vectorstores import FAISS
from sentence_transformers import CrossEncoder
import torch

from utils.langchain_wrappers import VertexAIEmbedding

load_dotenv()
FAISS_INDEX_DIR = "data/vector_store/faiss"

with open("data/chunks.pkl", 'rb') as file:
    DOCUMENTS = pickle.load(file)


def get_vector_store(documents=DOCUMENTS):
    embeddings = VertexAIEmbedding()
    vectorstore = FAISS.load_local(
        FAISS_INDEX_DIR, embeddings, allow_dangerous_deserialization=True
    )
    return vectorstore


def retrieve(query):
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 20,
        },
        search_type="similarity"
    )
    return retriever.get_relevant_documents(query)


def rerank(query, initial_docs, top_n=10):
    doc_pairs = [[query, doc.page_content] for doc in initial_docs]

    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    with torch.no_grad():
        scores = model.predict(doc_pairs)
    
    docs_with_scores = list(zip(initial_docs, scores))
    sorted_docs_with_scores = sorted(docs_with_scores, key=lambda x: x[1], reverse=True)
    
    reranked_docs = [doc for doc, score in sorted_docs_with_scores[:top_n]]
    
    return reranked_docs