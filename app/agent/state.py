from typing import TypedDict


class AgentState(TypedDict):
    question: str
    search_query: str
    search_results: list
    context: str
    answer: str
    retry_count: int
    results_relevant: bool