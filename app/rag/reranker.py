from sentence_transformers import CrossEncoder


class CodeReranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query,
        results,
        top_k=5
    ):

        if not results:
            return []

        pairs = []

        for result in results:

            code = result.get(
                "content",
                ""
            )

            metadata = (
                f"File: {result.get('file_path', '')}\n"
                f"Symbol: {result.get('symbol', '')}\n"
                f"Language: {result.get('language', '')}\n"
            )

            text = metadata + "\n" + code

            pairs.append(
                [query, text]
            )

        scores = self.model.predict(
            pairs
        )

        reranked = []

        for result, score in zip(
            results,
            scores
        ):

            result = result.copy()

            result["rerank_score"] = float(
                score
            )

            reranked.append(result)

        reranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked[:top_k]