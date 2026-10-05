
from pathlib import Path

from app.rag.loader import load_repository
from app.rag.chunker import chunk_repository


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_REPO = ROOT / "tests" / "fixtures" / "sample_repo"


def main():
    files = load_repository(str(SAMPLE_REPO))
    chunks = chunk_repository(files)

    print(f"\nFiles discovered: {len(files)}")
    print(f"Chunks created: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]

        print(f"\n--- Chunk {index} ---")
        print(f"File: {metadata['file_path']}")
        print(f"Symbol: {metadata['symbol']}")
        print(f"Type: {metadata['chunk_type']}")
        print(
            f"Lines: {metadata['start_line']}-"
            f"{metadata['end_line']}"
        )
        print(chunk["content"][:200])


if __name__ == "__main__":
    main()