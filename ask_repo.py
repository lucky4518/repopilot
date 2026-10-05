import sys

from app.agent.graph import create_graph


def main():

    if len(sys.argv) < 2:

        print(
            'Usage: python ask_repo.py "your question"'
        )

        return

    question = " ".join(
        sys.argv[1:]
    )

    graph = create_graph()

    result = graph.invoke(
        {
            "question": question,
            "search_query": question,
            "search_results": [],
            "context": "",
            "answer": "",
            "retry_count": 0,
            "results_relevant": False
        }
    )

    print()
    print("=" * 70)
    print("RepoPilot")
    print("=" * 70)

    print()
    print("Question:")
    print(question)

    print()
    print("Answer:")
    print(result["answer"])


if __name__ == "__main__":
    main()