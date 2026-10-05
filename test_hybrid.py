from app.rag.bm25 import BM25Index


chunks = [
    {
        "content": """
def login_user(username, password):
    user = find_user(username)
    return verify_password(user, password)
""",
        "metadata": {
            "file_path": "auth/login.py",
            "language": "python",
            "symbol": "login_user",
            "chunk_type": "function",
            "start_line": 1,
            "end_line": 4
        }
    },

    {
        "content": """
def calculate_tax(income):
    return income * 0.18
""",
        "metadata": {
            "file_path": "finance/tax.py",
            "language": "python",
            "symbol": "calculate_tax",
            "chunk_type": "function",
            "start_line": 1,
            "end_line": 2
        }
    },

    {
        "content": """
JWT_SECRET = "secret"

def generate_token(user):
    return create_jwt(user, JWT_SECRET)
""",
        "metadata": {
            "file_path": "auth/jwt.py",
            "language": "python",
            "symbol": "generate_token",
            "chunk_type": "function",
            "start_line": 1,
            "end_line": 4
        }
    }
]


index = BM25Index()

index.build(chunks)

query = "JWT_SECRET"

results = index.search(
    query,
    top_k=3
)

print()
print("=" * 70)
print("BM25 SEARCH")
print("=" * 70)

print()
print("Query:", query)

for i, result in enumerate(
    results,
    start=1
):

    chunk = result["chunk"]
    metadata = chunk["metadata"]

    print()
    print(f"RESULT {i}")
    print("-" * 70)

    print(
        "Score:",
        result["score"]
    )

    print(
        "File:",
        metadata["file_path"]
    )

    print(
        "Symbol:",
        metadata["symbol"]
    )

    print()
    print(chunk["content"])