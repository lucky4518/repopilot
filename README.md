# 🚀 RepoPilot — Agentic Codebase Intelligence Platform

RepoPilot is an **agentic codebase intelligence platform** that helps developers understand and search large software repositories using **code-aware RAG, hybrid retrieval, reranking, and LangGraph-based agentic workflows**.

Instead of relying only on semantic vector search, RepoPilot combines **dense vector retrieval with BM25 keyword search**, merges the results using **Reciprocal Rank Fusion (RRF)**, and then applies a **cross-encoder reranker** to improve the relevance of retrieved code.

The project also includes an **MCP-based tool server** for exposing repository operations such as code search, file reading, and symbol lookup.

---

## ✨ Features

* **Repository ingestion**

  * Scans supported source-code and documentation files.
  * Ignores unnecessary directories such as `.git`, virtual environments, build directories, and `node_modules`.

* **Code-aware chunking**

  * Uses Python AST parsing to identify classes, functions, and methods.
  * Preserves metadata such as file path, symbol name, chunk type, and line numbers.
  * Uses line-based chunking as a fallback for unsupported or syntactically invalid Python files.

* **Vector search**

  * Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
  * Stores embeddings locally using Qdrant.
  * Uses cosine similarity for semantic retrieval.

* **BM25 keyword search**

  * Provides lexical retrieval for exact identifiers, function names, filenames, and technical terms.
  * Particularly useful for code-specific queries where exact token matching matters.

* **Hybrid retrieval**

  * Combines vector and BM25 results.
  * Uses Reciprocal Rank Fusion (RRF) to produce a unified ranking.

* **Cross-encoder reranking**

  * Uses `cross-encoder/ms-marco-MiniLM-L-6-v2` to rerank retrieved candidates according to the query.

* **Agentic retrieval**

  * Uses LangGraph to orchestrate repository search and answer generation.
  * Supports query rewriting when the initial retrieval is insufficient.

* **LLM-powered code understanding**

  * Uses an OpenRouter-hosted LLM to generate grounded answers from retrieved repository context.
  * The system is instructed not to invent repository files, symbols, or behavior.

* **MCP tools**

  * Provides an MCP server exposing repository operations:

    * `search_repository`
    * `read_file`
    * `find_symbol`

* **Interactive UI**

  * Streamlit interface for asking questions about the indexed repository.
  * Displays retrieved files, symbols, line ranges, and retrieval scores.

---

## 🏗️ Architecture

```text
                         User
                          │
                          ▼
                   ┌──────────────┐
                   │  Streamlit   │
                   │      UI      │
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  LangGraph   │
                   │    Agent     │
                   └──────┬───────┘
                          │
                          ▼
                  ┌─────────────────┐
                  │ Hybrid Retrieval│
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │ Vector Search│          │ BM25 Search  │
       │   Qdrant     │          │              │
       └──────┬───────┘          └──────┬───────┘
              │                         │
              └───────────┬─────────────┘
                          ▼
                   ┌─────────────┐
                   │ RRF Fusion  │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Cross Encoder│
                   │  Reranker   │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Context   │
                   └──────┬──────┘
                          │
                          ▼
                     ┌─────────┐
                     │   LLM   │
                     └────┬────┘
                          │
                          ▼
                       Answer
```

---

## 🔍 Retrieval Pipeline

RepoPilot uses a multi-stage retrieval pipeline.

### 1. Repository Loading

Supported files are loaded from the repository while ignoring directories such as:

```text
.git
.venv
venv
node_modules
__pycache__
dist
build
.next
vendor
```

### 2. Code-Aware Chunking

Python files are parsed using the Python AST.

For example:

```python
class UserService:

    def create_user(self):
        ...
```

can produce chunks with metadata such as:

```text
File: services/user.py
Symbol: UserService
Type: class
Lines: 1-20
```

and:

```text
File: services/user.py
Symbol: UserService.create_user
Type: method
Lines: 5-10
```

This metadata allows retrieval to preserve the structure of the source code.

### 3. Dense Retrieval

Each chunk is converted into an embedding using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embeddings are stored in:

```text
Qdrant
```

using cosine similarity.

### 4. BM25 Retrieval

The same chunks are indexed using BM25.

This helps retrieve exact code identifiers such as:

```text
VectorStore
query_points
HybridRetriever
create_graph
```

which may not always be retrieved optimally through semantic similarity alone.

### 5. Reciprocal Rank Fusion

The vector and BM25 rankings are combined using RRF:

```text
RRF score = Σ 1 / (k + rank)
```

This produces a unified candidate set.

### 6. Cross-Encoder Reranking

The candidate chunks are then passed through:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

The reranker evaluates the relationship between the user's query and each retrieved code chunk and produces the final ranking.

---

## 🤖 Agentic Workflow

The LangGraph workflow coordinates the retrieval process.

```text
                    Question
                       │
                       ▼
                    Search
                       │
                       ▼
                 Evaluate Results
                    /        \
                   /          \
              Relevant      Not Relevant
                 │               │
                 ▼               ▼
              Context       Rewrite Query
                 │               │
                 │               ▼
                 │             Search
                 │               │
                 └───────┬───────┘
                         ▼
                       Answer
```

The query rewriting stage allows the agent to transform a broad natural-language question into a more code-oriented search query.

For example:

```text
Original:
How does vector search work?

Rewritten:
VectorStore Qdrant query_points embedding search CodeRetriever
```

---

## 🧰 MCP Server

RepoPilot also contains an MCP server that exposes repository capabilities as tools.

Available tools include:

```text
search_repository()
read_file()
find_symbol()
```

### `search_repository()`

Searches the indexed repository using the hybrid retrieval pipeline.

### `read_file()`

Reads a file from the repository while preventing access outside the repository root.

### `find_symbol()`

Searches the repository for occurrences of a class, function, variable, or other symbol.

The MCP layer is designed to allow external MCP-compatible agents or clients to interact with RepoPilot's repository capabilities through standardized tools.

---

## 🖥️ User Interface

RepoPilot provides a Streamlit interface for interacting with the agent.

The UI allows users to:

* Enter repository questions.
* Run the LangGraph agent.
* View generated answers.
* Inspect retrieved files.
* Inspect symbols and line ranges.
* View hybrid and reranking scores.
* Inspect the code chunks used to generate an answer.

Start the UI with:

```bash
streamlit run ui.py
```

Then open the local Streamlit URL shown in the terminal.

---

## 📁 Project Structure

```text
RepoPilot/
│
├── app/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   ├── state.py
│   │   └── mcp_tools.py
│   │
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── server.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── indexer.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── bm25.py
│   │   ├── hybrid_retriever.py
│   │   └── reranker.py
│   │
│   └── services/
│       ├── __init__.py
│       └── llm.py
│
├── data/
│   ├── qdrant/
│   └── bm25.pkl
│
├── ask_repo.py
├── index_repo.py
├── search_repo.py
├── test_mcp_client.py
├── test_ingestion.py
├── test_llm.py
├── ui.py
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository and enter the project directory:

```bash
cd RepoPilot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

If dependencies are being installed individually during development:

```bash
pip install qdrant-client
pip install sentence-transformers
pip install rank-bm25
pip install langgraph
pip install langchain-openai
pip install python-dotenv
pip install streamlit
pip install fastmcp
pip install langchain-mcp-adapters
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```text
OPENROUTER_API_KEY=your_api_key_here
```

RepoPilot uses OpenRouter to access the configured LLM.

Do not commit `.env` to Git.

---

## 📚 Index a Repository

Before asking questions, index the target repository:

```bash
python index_repo.py "D:\path\to\repository"
```

The indexer performs:

```text
Repository
    ↓
File Loading
    ↓
Code Chunking
    ↓
Embeddings
    ↓
Qdrant
    +
BM25
```

---

## 🔎 Search the Repository

You can directly test the hybrid retrieval system:

```bash
python search_repo.py "how are code chunks created"
```

Another example:

```bash
python search_repo.py "how does vector search work"
```

The search output includes:

* File path
* Symbol
* Chunk type
* Line range
* Hybrid score
* Reranker score
* Retrieved code

---

## 🤖 Ask RepoPilot

You can interact with the LangGraph agent from the command line:

```bash
python ask_repo.py "how does vector search work?"
```

Example questions:

```text
How are Python functions converted into chunks?

How does BM25 search work?

How are vector search and BM25 combined?

How does the reranker select results?

How does the LangGraph agent retry a search?
```

---

## 🖥️ Start the UI

Run:

```bash
streamlit run ui.py
```

The application will be available through the local Streamlit URL displayed in the terminal.

---

## 🧪 MCP Server

Start the MCP server with:

```bash
python -m app.mcp.server
```

The server exposes:

```text
search_repository
read_file
find_symbol
```

MCP client integration is currently an additional interface for exposing RepoPilot repository capabilities.

---

## 🛠️ Technology Stack

| Component              | Technology             |
| ---------------------- | ---------------------- |
| Language               | Python                 |
| Agent orchestration    | LangGraph              |
| LLM access             | OpenRouter             |
| Embeddings             | Sentence Transformers  |
| Vector database        | Qdrant                 |
| Keyword retrieval      | BM25                   |
| Result fusion          | Reciprocal Rank Fusion |
| Reranking              | Cross-Encoder          |
| MCP server             | FastMCP                |
| UI                     | Streamlit              |
| Environment management | python-dotenv          |

---

## 🎯 Example Use Cases

RepoPilot can help answer questions such as:

```text
Where is authentication implemented?

How does the application perform database queries?

Which class handles API requests?

How are documents indexed?

Where is a particular function used?

How does the retrieval pipeline work?

Which files are responsible for generating embeddings?

How does the agent handle failed retrieval?
```

---

## 🔮 Future Improvements

Potential extensions include:

* More advanced code-aware chunking for additional languages.
* AST-based symbol indexing.
* Graph-based code relationships.
* Improved relevance grading.
* Multi-query retrieval.
* Query decomposition for complex questions.
* Repository-level dependency analysis.
* Test execution through agent tools.
* Git-aware code analysis.
* Better MCP client integration.
* Persistent conversation history.
* Streaming agent responses.
* Repository indexing and re-indexing directly from the UI.

---

## 📌 Project Goal

RepoPilot is designed as a practical exploration of how **RAG, hybrid information retrieval, reranking, agentic workflows, and tool-based repository interaction** can be combined to build an AI assistant specifically for software repositories.
