from pathlib import Path

from fastmcp import FastMCP


mcp = FastMCP(
    "RepoPilot"
)


# ---------------------------------------------------------
# Repository root
# ---------------------------------------------------------

REPO_ROOT = Path(
    __file__
).resolve().parents[2]


# ---------------------------------------------------------
# Tool 1: Search repository
# ---------------------------------------------------------

@mcp.tool()
def search_repository(
    query: str,
    top_k: int = 5
) -> str:
    """
    Search the indexed repository using
    RepoPilot's hybrid retrieval system.
    """

    from app.rag.vector_store import VectorStore
    from app.rag.retriever import CodeRetriever
    from app.rag.hybrid_retriever import HybridRetriever

    vector_store = VectorStore()

    try:

        vector_retriever = CodeRetriever(
            vector_store
        )

        hybrid_retriever = HybridRetriever(
            vector_retriever
        )

        results = hybrid_retriever.retrieve(
            query=query,
            top_k=top_k,
            vector_k=10,
            bm25_k=10,
            rerank_k=10
        )

        if not results:
            return "No relevant code found."

        output = []

        for i, result in enumerate(
            results,
            start=1
        ):

            output.append(
                f"""
RESULT {i}

File:
{result['file_path']}

Symbol:
{result['symbol']}

Type:
{result['chunk_type']}

Lines:
{result['start_line']}-{result['end_line']}

Score:
{result.get('rerank_score', 0)}

Code:
{result['content']}
"""
            )

        return "\n".join(output)

    finally:

        vector_store.close()


# ---------------------------------------------------------
# Tool 2: Read file
# ---------------------------------------------------------

@mcp.tool()
def read_file(
    file_path: str
) -> str:
    """
    Read a repository file.
    """

    root = REPO_ROOT.resolve()

    requested_path = (
        root / file_path
    ).resolve()

    # Prevent path traversal
    if root not in requested_path.parents:
        return "Error: Access outside repository is not allowed."

    if not requested_path.exists():
        return f"File not found: {file_path}"

    if not requested_path.is_file():
        return f"Not a file: {file_path}"

    try:

        return requested_path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        return "Error: File is not valid UTF-8."


# ---------------------------------------------------------
# Tool 3: Find symbol
# ---------------------------------------------------------

@mcp.tool()
def find_symbol(
    symbol: str
) -> str:
    """
    Find occurrences of a symbol in the repository.
    """

    from app.rag.loader import load_repository

    files = load_repository(
        str(REPO_ROOT)
    )

    matches = []

    for file_record in files:

        content = file_record["content"]

        if symbol.lower() in content.lower():

            lines = content.splitlines()

            matching_lines = []

            for number, line in enumerate(
                lines,
                start=1
            ):

                if symbol.lower() in line.lower():

                    matching_lines.append(
                        f"{number}: {line}"
                    )

            matches.append(
                f"""
File:
{file_record['file_path']}

Matches:
{chr(10).join(matching_lines[:20])}
"""
            )

    if not matches:
        return f"No occurrences found for symbol: {symbol}"

    return "\n".join(matches)


# ---------------------------------------------------------
# Run MCP server
# ---------------------------------------------------------

if __name__ == "__main__":

    mcp.run()