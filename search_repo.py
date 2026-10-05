import sys

from app.rag.vector_store import VectorStore
from app.rag.retriever import CodeRetriever
from app.rag.hybrid_retriever import HybridRetriever


def main():

    if len(sys.argv) < 2:

        print(
            'Usage: python search_repo.py "your query"'
        )

        return

    query = " ".join(
        sys.argv[1:]
    )

    vector_store = VectorStore()

    vector_retriever = CodeRetriever(
        vector_store
    )

    hybrid_retriever = HybridRetriever(
        vector_retriever
    )

    try:

        results = hybrid_retriever.retrieve(
            query=query,
            top_k=5,
            vector_k=10,
            bm25_k=10,
            rerank_k=10
        )

        print()
        print("=" * 70)
        print("RepoPilot Hybrid Code Search")
        print("=" * 70)

        print()
        print("Query:")
        print(query)

        print()
        print(
            f"Found {len(results)} results."
        )

        for i, result in enumerate(
            results,
            start=1
        ):

            print()
            print("=" * 70)
            print(f"RESULT {i}")
            print("=" * 70)

            print(
                f"Hybrid Score: "
                f"{result['hybrid_score']:.6f}"
            )

            print(
                f"Rerank Score: "
                f"{result['rerank_score']:.6f}"
            )

            print(
                f"File: "
                f"{result['file_path']}"
            )

            print(
                f"Symbol: "
                f"{result['symbol']}"
            )

            print(
                f"Type: "
                f"{result['chunk_type']}"
            )

            print(
                f"Lines: "
                f"{result['start_line']}-"
                f"{result['end_line']}"
            )

            print()
            print("Code:")
            print(
                result["content"]
            )

    finally:

        vector_store.close()


if __name__ == "__main__":
    main()