from app.rag.bm25 import BM25Index
from app.rag.reranker import CodeReranker


class HybridRetriever:

    def __init__(self, vector_retriever):

        self.vector_retriever = vector_retriever
        self.bm25 = BM25Index()
        self.reranker = CodeReranker()

    def retrieve(
        self,
        query,
        top_k=5,
        vector_k=10,
        bm25_k=10,
        rerank_k=10
    ):

        # -------------------------
        # Vector Search
        # -------------------------

        vector_results = (
            self.vector_retriever.retrieve(
                query=query,
                top_k=vector_k
            )
        )

        # -------------------------
        # BM25 Search
        # -------------------------

        bm25_results = self.bm25.search(
            query=query,
            top_k=bm25_k
        )

        # -------------------------
        # RRF Fusion
        # -------------------------

        fused_results = self._rrf_fusion(
            vector_results,
            bm25_results,
            rerank_k
        )

        # -------------------------
        # Reranking
        # -------------------------

        final_results = self.reranker.rerank(
            query=query,
            results=fused_results,
            top_k=top_k
        )

        return final_results

    def _rrf_fusion(
        self,
        vector_results,
        bm25_results,
        top_k
    ):

        RRF_K = 60

        scores = {}
        chunks = {}

        # Vector results
        for rank, result in enumerate(
            vector_results,
            start=1
        ):

            key = self._result_key(result)

            scores[key] = (
                scores.get(key, 0)
                + 1 / (RRF_K + rank)
            )

            chunks[key] = result

        # BM25 results
        for rank, result in enumerate(
            bm25_results,
            start=1
        ):

            converted = self._convert_chunk(
                result["chunk"]
            )

            key = self._result_key(converted)

            scores[key] = (
                scores.get(key, 0)
                + 1 / (RRF_K + rank)
            )

            chunks[key] = converted

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for key, score in ranked[:top_k]:

            result = chunks[key].copy()

            result["hybrid_score"] = score

            results.append(result)

        return results

    def _result_key(self, result):

        return (
            result.get("file_path", ""),
            result.get("start_line", 0),
            result.get("end_line", 0)
        )

    def _convert_chunk(self, chunk):

        metadata = chunk.get(
            "metadata",
            {}
        )

        return {
            "content": chunk.get(
                "content",
                ""
            ),
            "file_path": metadata.get(
                "file_path",
                ""
            ),
            "language": metadata.get(
                "language",
                ""
            ),
            "symbol": metadata.get(
                "symbol",
                ""
            ),
            "chunk_type": metadata.get(
                "chunk_type",
                ""
            ),
            "start_line": metadata.get(
                "start_line",
                0
            ),
            "end_line": metadata.get(
                "end_line",
                0
            )
        }