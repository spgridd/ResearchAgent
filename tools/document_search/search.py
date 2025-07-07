from utils.vectorstore import retrieve, rerank

def document_search(query: str) -> dict:
    """
        Search through document titled: "IFC Annual Report 2024 financials" 
        to find relevant chunks for given user query.

        Args:
            query: Question from the user about the document.

        Returns:
            dict: List of retrieved chunks.
    """
    context = retrieve(query)
    context = rerank(query, context)

    return {"context": context}