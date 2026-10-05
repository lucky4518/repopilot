from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.agent.state import AgentState

from app.agent.nodes import (
    search_code,
    evaluate_results,
    rewrite_query,
    build_context,
    generate_answer
)


def route_after_evaluation(state):

    if state["results_relevant"]:
        return "context"

    if state.get("retry_count", 0) >= 1:
        return "context"

    return "rewrite"


def create_graph():

    graph = StateGraph(
        AgentState
    )

    graph.add_node(
        "search",
        search_code
    )

    graph.add_node(
        "evaluate",
        evaluate_results
    )

    graph.add_node(
        "rewrite",
        rewrite_query
    )

    graph.add_node(
        "context",
        build_context
    )

    graph.add_node(
        "answer",
        generate_answer
    )

    graph.add_edge(
        START,
        "search"
    )

    graph.add_edge(
        "search",
        "evaluate"
    )

    graph.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {
            "context": "context",
            "rewrite": "rewrite"
        }
    )

    graph.add_edge(
        "rewrite",
        "search"
    )

    graph.add_edge(
        "context",
        "answer"
    )

    graph.add_edge(
        "answer",
        END
    )

    return graph.compile()