from app.rag.vector_store import VectorStore
from app.rag.bm25 import BM25Index


class RepositoryIndexer:

    def __init__(self):

        self.vector_store = VectorStore()
        self.bm25 = BM25Index()

    def index(
        self,
        chunks,
        clear_existing=False
    ):

        if not chunks:

            print("No chunks found.")
            return

        if clear_existing:

            print(
                "Clearing existing Qdrant collection..."
            )

            self.vector_store.clear()

        print(
            f"Starting indexing of {len(chunks)} chunks..."
        )

        # -------------------------
        # Vector Search Index
        # -------------------------

        self.vector_store.add_chunks(
            chunks
        )

        # -------------------------
        # BM25 Index
        # -------------------------

        print(
            "Building BM25 index..."
        )

        self.bm25.build(
            chunks
        )

        self.bm25.save()

        print(
            "Repository indexing completed."
        )

        print(
            f"Total vectors in Qdrant: "
            f"{self.vector_store.count()}"
        )

    def count(self):

        return self.vector_store.count()

    def close(self):

        self.vector_store.close()