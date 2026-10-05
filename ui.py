import streamlit as st

from app.agent.graph import create_graph


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RepoPilot",
    page_icon="🚀",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🚀 RepoPilot")

st.caption(
    "Agentic Codebase Intelligence & Automation Platform"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Repository")

    repo_path = st.text_input(
        "Repository Path",
        placeholder=r"D:\projects\my_project"
    )

    st.divider()

    st.subheader("System")

    st.success("✓ Qdrant")
    st.success("✓ BM25")
    st.success("✓ Reranker")
    st.success("✓ LangGraph")

    st.divider()

    st.caption(
        "RepoPilot uses hybrid code retrieval "
        "with agentic query refinement."
    )


# =========================================================
# MAIN AREA
# =========================================================

st.subheader("Ask your codebase")

question = st.text_area(
    "Question",
    placeholder=(
        "Example: How does vector search work "
        "in this repository?"
    ),
    height=100
)


ask_button = st.button(
    "🔍 Ask RepoPilot",
    type="primary"
)


# =========================================================
# ASK
# =========================================================

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "RepoPilot is analyzing the codebase..."
        ):

            try:

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

                # =========================================
                # ANSWER
                # =========================================

                st.subheader("Answer")

                st.write(
                    result["answer"]
                )

                # =========================================
                # DEBUG / RETRIEVAL INFORMATION
                # =========================================

                st.divider()

                st.subheader(
                    "Retrieved Code"
                )

                results = result.get(
                    "search_results",
                    []
                )

                if results:

                    for i, item in enumerate(
                        results,
                        start=1
                    ):

                        with st.expander(
                            f"{i}. {item['file_path']} "
                            f"— {item['symbol']}"
                        ):

                            col1, col2 = st.columns(2)

                            with col1:

                                st.write(
                                    f"**Type:** "
                                    f"{item['chunk_type']}"
                                )

                                st.write(
                                    f"**Lines:** "
                                    f"{item['start_line']}-"
                                    f"{item['end_line']}"
                                )

                            with col2:

                                st.write(
                                    f"**Hybrid Score:** "
                                    f"{item.get('hybrid_score', 0):.4f}"
                                )

                                st.write(
                                    f"**Rerank Score:** "
                                    f"{item.get('rerank_score', 0):.4f}"
                                )

                            st.code(
                                item["content"],
                                language=item.get(
                                    "language",
                                    "text"
                                )
                            )

                else:

                    st.info(
                        "No retrieval results available."
                    )

            except Exception as e:

                st.error(
                    "RepoPilot encountered an error."
                )

                st.exception(e)