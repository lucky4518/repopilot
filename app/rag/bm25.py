from pathlib import Path
import pickle
import re

from rank_bm25 import BM25Okapi


class BM25Index:

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        self.data_dir = project_root / "data"
        self.data_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.index_path = (
            self.data_dir / "bm25.pkl"
        )

        self.chunks = []
        self.tokenized_chunks = []
        self.bm25 = None

    def tokenize(self, text):

        return re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*|\d+",
            text.lower()
        )

    def _prepare_text(self, chunk):

        metadata = chunk.get(
            "metadata",
            {}
        )

        return f"""
        {metadata.get("file_path", "")}
        {metadata.get("language", "")}
        {metadata.get("symbol", "")}
        {metadata.get("chunk_type", "")}
        {chunk.get("content", "")}
        """

    def build(self, chunks):

        self.chunks = chunks

        self.tokenized_chunks = [
            self.tokenize(
                self._prepare_text(chunk)
            )
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_chunks
        )

    def save(self):

        data = {
            "chunks": self.chunks,
            "tokenized_chunks": self.tokenized_chunks
        }

        with open(
            self.index_path,
            "wb"
        ) as file:

            pickle.dump(
                data,
                file
            )

        print(
            f"BM25 index saved to {self.index_path}"
        )

    def load(self):

        if not self.index_path.exists():

            raise FileNotFoundError(
                "BM25 index not found. "
                "Run index_repo.py first."
            )

        with open(
            self.index_path,
            "rb"
        ) as file:

            data = pickle.load(file)

        self.chunks = data["chunks"]

        self.tokenized_chunks = (
            data["tokenized_chunks"]
        )

        self.bm25 = BM25Okapi(
            self.tokenized_chunks
        )

    def search(
        self,
        query,
        top_k=10
    ):

        if self.bm25 is None:

            self.load()

        query_tokens = self.tokenize(
            query
        )

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indices:

            results.append({
                "chunk": self.chunks[index],
                "score": float(scores[index])
            })

        return results