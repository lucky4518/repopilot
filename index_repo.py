import sys

from app.rag.loader import load_repository
from app.rag.chunker import chunk_repository
from app.rag.indexer import RepositoryIndexer


def main():

    # ==================================================
    # CHECK ARGUMENT
    # ==================================================

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python index_repo.py <repository_path>"
        )

        return

    repo_path = sys.argv[1]

    print()
    print("=" * 70)
    print("RepoPilot Repository Indexer")
    print("=" * 70)

    print()
    print(
        f"Repository: {repo_path}"
    )

    # ==================================================
    # STEP 1: LOAD REPOSITORY
    # ==================================================

    print()
    print("[1/3] Loading repository...")

    files = load_repository(
        repo_path
    )

    print(
        f"Loaded {len(files)} files."
    )

    # ==================================================
    # STEP 2: CREATE CODE CHUNKS
    # ==================================================

    print()
    print("[2/3] Creating code chunks...")

    chunks = chunk_repository(
        files
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    # ==================================================
    # STEP 3: INDEX INTO QDRANT
    # ==================================================

    print()
    print("[3/3] Indexing chunks into Qdrant...")

    indexer = RepositoryIndexer()

    try:

        indexer.index(
            chunks,
            clear_existing=True
        )

    finally:

        indexer.close()

    # ==================================================
    # COMPLETE
    # ==================================================

    print()
    print("=" * 70)
    print("Repository indexing completed successfully.")
    print("=" * 70)


if __name__ == "__main__":

    main()