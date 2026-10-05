from app.rag.vector_store import VectorStore
from app.rag.retriever import CodeRetriever


class CodeSearch:

    def __init__(self, chunks):

        # --------------------------------------------------
        # Create vector store
        # --------------------------------------------------

        self.vector_store = VectorStore()

        # --------------------------------------------------
        # Add repository chunks
        # --------------------------------------------------

        self.vector_store.add_chunks(chunks)

        # --------------------------------------------------
        # Create retriever
        # --------------------------------------------------

        self.retriever = CodeRetriever(
            self.vector_store
        )

    # ======================================================
    # SEARCH REPOSITORY
    # ======================================================

    def search(self, query, top_k=5):

        return self.retriever.retrieve(
            query=query,
            top_k=top_k
        )