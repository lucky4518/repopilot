from app.rag.vector_store import VectorStore
from app.rag.retriever import CodeRetriever
from app.rag.hybrid_retriever import HybridRetriever
from app.services.llm import get_llm


vector_store = VectorStore()

vector_retriever = CodeRetriever(
    vector_store
)

hybrid_retriever = HybridRetriever(
    vector_retriever
)

llm = get_llm()


def search_code(state):

    query = state.get(
        "search_query",
        state["question"]
    )

    results = hybrid_retriever.retrieve(
        query=query,
        top_k=5,
        vector_k=10,
        bm25_k=10,
        rerank_k=10
    )

    return {
        "search_results": results
    }


def evaluate_results(state):

    results = state["search_results"]

    if not results:
        return {
            "results_relevant": False
        }

    # For now, use the reranker score as a basic signal.
    best_score = results[0].get(
        "rerank_score",
        0
    )

    relevant = best_score > 0

    return {
        "results_relevant": relevant
    }


def rewrite_query(state):

    question = state["question"]

    retry_count = state.get(
        "retry_count",
        0
    )

    prompt = f"""
You are a code search query optimizer.

The user's original question is:

{question}

The previous repository search did not retrieve
useful enough information.

Rewrite the question into a precise technical
search query that is likely to find the relevant
code.

Focus on:
- class names
- function names
- files
- libraries
- technical operations
- implementation details

Return ONLY the rewritten search query.

Example:

User question:
How does vector search work?

Better search query:
VectorStore Qdrant query_points embedding search CodeRetriever
"""

    response = llm.invoke(prompt)

    rewritten_query = response.content.strip()

    return {
        "search_query": rewritten_query,
        "retry_count": retry_count + 1
    }


def build_context(state):

    results = state["search_results"]

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
File: {result['file_path']}
Symbol: {result['symbol']}
Type: {result['chunk_type']}
Lines: {result['start_line']}-{result['end_line']}

Code:
{result['content']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    return {
        "context": context
    }


def generate_answer(state):

    question = state["question"]
    context = state["context"]

    prompt = f"""
You are RepoPilot, an AI codebase assistant.

Answer the user's question using ONLY the provided
repository context.

Rules:

1. Do not invent files, functions, classes, or behavior.
2. Mention relevant file paths.
3. Mention symbols/functions/classes when useful.
4. Explain the implementation clearly.
5. If the context is insufficient, say so explicitly.
6. Do not claim that code exists if it is not present
   in the provided context.

Repository Context:
-------------------

{context}

User Question:
--------------

{question}
"""

    response = llm.invoke(
        prompt
    )

    return {
        "answer": response.content
    }