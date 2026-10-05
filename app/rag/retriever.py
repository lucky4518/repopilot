from app.rag.vector_store import VectorStore


class CodeRetriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store

    # ======================================================
    # RETRIEVE RELEVANT CODE
    # ======================================================

    def retrieve(self, query, top_k=5):

        results = self.vector_store.search(
            query=query,
            limit=top_k
        )

        retrieved_chunks = []

        for result in results:

            payload = result.payload

            chunk = {
                "score": result.score,
                "file_path": payload.get("file_path"),
                "language": payload.get("language"),
                "symbol": payload.get("symbol"),
                "chunk_type": payload.get("chunk_type"),
                "start_line": payload.get("start_line"),
                "end_line": payload.get("end_line"),
                "content": payload.get("content")
            }

            retrieved_chunks.append(chunk)

        return retrieved_chunks