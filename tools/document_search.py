from utils.vectorstore import retrieve, rerank
from langfuse.decorators import observe

@observe
def document_search(query: str) -> dict:
    """
        Search through document titled: "IFC Annual Report 2024 financials" 
        to find relevant chunks for given user query.

        Args:
            query: Exact part of the question from the user about the document (if given filters include them).

        Returns:
            dict: List of retrieved chunks.
    """
    context = retrieve(query)
    context = rerank(query, context)

    return {"context": context}