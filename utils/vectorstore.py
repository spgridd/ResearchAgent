from dotenv import load_dotenv
import pickle
from langchain_community.vectorstores import FAISS
from sentence_transformers import CrossEncoder
import torch
import logging

from utils.langchain_wrappers import VertexAIEmbedding
from utils.prompt_filter import get_faiss_filter, extract_filters

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
    filters = extract_filters(query)
    _, any_flag = get_faiss_filter(filters)
    specific_filter, _ = get_faiss_filter(filters)

    if specific_filter != {}:
        if any_flag:
            retrieval_plan = [
                {'content_type': 'text', 'k': 10},
                {'content_type': 'table', 'k': 10},
                {'content_type': 'image', 'k': 5},
            ]
            
            all_retrieved_docs = []
            for plan in retrieval_plan:
                content_type, k = plan['content_type'], plan['k']
                
                specific_filter, _ = get_faiss_filter(filters, force_content_type=content_type)
                
                temp_retriever = vector_store.as_retriever(
                    search_kwargs={'k': k, 'filter': specific_filter}
                )
                
                all_retrieved_docs.extend(temp_retriever.invoke(query))

            unique_docs = {}
            for doc in all_retrieved_docs:
                if 'chunk_id' in doc.metadata:
                    unique_docs[doc.metadata['chunk_id']] = doc
            
            return list(unique_docs.values())
    
    retriever = vector_store.as_retriever(
        search_kwargs={'k': 25, 'filter': specific_filter}
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
