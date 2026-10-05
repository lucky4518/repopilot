from pathlib import Path
import hashlib

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):

        # ==================================================
        # PROJECT ROOT
        # ==================================================

        project_root = Path(__file__).resolve().parents[2]

        # ==================================================
        # QDRANT STORAGE
        # ==================================================

        qdrant_path = project_root / "data" / "qdrant"

        qdrant_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==================================================
        # QDRANT CLIENT
        # ==================================================

        self.client = QdrantClient(
            path=str(qdrant_path)
        )

        # ==================================================
        # COLLECTION
        # ==================================================

        self.collection_name = "repo_code"

        # ==================================================
        # EMBEDDING MODEL
        # ==================================================

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # ==================================================
        # CREATE COLLECTION
        # ==================================================

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in collection_names:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

    # ======================================================
    # PREPARE TEXT FOR EMBEDDING
    # ======================================================

    def _prepare_text(self, chunk):

        metadata = chunk.get(
            "metadata",
            {}
        )

        file_path = metadata.get(
            "file_path",
            ""
        )

        language = metadata.get(
            "language",
            ""
        )

        symbol = metadata.get(
            "symbol",
            ""
        )

        chunk_type = metadata.get(
            "chunk_type",
            ""
        )

        start_line = metadata.get(
            "start_line",
            ""
        )

        end_line = metadata.get(
            "end_line",
            ""
        )

        content = chunk.get(
            "content",
            ""
        )

        text = f"""
File: {file_path}

Language: {language}

Symbol: {symbol}

Chunk Type: {chunk_type}

Lines: {start_line}-{end_line}

Code:
{content}
"""

        return text

    # ======================================================
    # CREATE UNIQUE ID
    # ======================================================

    def _create_id(self, chunk):

        metadata = chunk.get(
            "metadata",
            {}
        )

        unique_string = (
            metadata.get("file_path", "")
            + str(metadata.get("start_line", ""))
            + str(metadata.get("end_line", ""))
            + chunk.get("content", "")
        )

        hash_value = hashlib.md5(
            unique_string.encode("utf-8")
        ).hexdigest()

        return hash_value

    # ======================================================
    # ADD CHUNKS
    # ======================================================

    def add_chunks(self, chunks):

        if not chunks:

            print("No chunks to index.")

            return

        points = []

        for chunk in chunks:

            # --------------------------------------------------
            # Prepare text
            # --------------------------------------------------

            text = self._prepare_text(
                chunk
            )

            # --------------------------------------------------
            # Generate embedding
            # --------------------------------------------------

            vector = self.model.encode(
                text
            ).tolist()

            # --------------------------------------------------
            # Create deterministic ID
            # --------------------------------------------------

            point_id = self._create_id(
                chunk
            )

            # --------------------------------------------------
            # Create Qdrant point
            # --------------------------------------------------

            point = PointStruct(
                id=point_id,
                vector=vector,
                payload=chunk
            )

            points.append(point)

        # --------------------------------------------------
        # Insert / update vectors
        # --------------------------------------------------

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(
            f"Added {len(points)} chunks to Qdrant."
        )

    # ======================================================
    # SEARCH
    # ======================================================

    def search(
        self,
        query,
        limit=5
    ):

        query_vector = self.model.encode(
            query
        ).tolist()

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )

        return results.points

    # ======================================================
    # COUNT
    # ======================================================

    def count(self):

        result = self.client.count(
            collection_name=self.collection_name
        )

        return result.count

    # ======================================================
    # CLEAR COLLECTION
    # ======================================================

    def clear(self):

        self.client.delete_collection(
            collection_name=self.collection_name
        )

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    # ======================================================
    # CLOSE
    # ======================================================

    def close(self):

        self.client.close()