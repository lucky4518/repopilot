from app.rag.vector_store import VectorStore


# ==========================================================
# SAMPLE CODE CHUNKS
# ==========================================================

chunks = [

    {
        "file_path": "auth/login.py",
        "language": "python",
        "symbol": "login_user",
        "chunk_type": "function",
        "start_line": 1,
        "end_line": 10,
        "content": """
def login_user(username, password):
    user = find_user(username)

    if user and check_password(password, user.password):
        return create_session(user)

    return None
"""
    },

    {
        "file_path": "database/user.py",
        "language": "python",
        "symbol": "find_user",
        "chunk_type": "function",
        "start_line": 1,
        "end_line": 8,
        "content": """
def find_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    return database.execute(query, username)
"""
    },

    {
        "file_path": "api/routes.py",
        "language": "python",
        "symbol": "get_users",
        "chunk_type": "function",
        "start_line": 20,
        "end_line": 30,
        "content": """
@app.route("/users")
def get_users():
    users = User.get_all()

    return jsonify(users)
"""
    },

    {
        "file_path": "auth/password.py",
        "language": "python",
        "symbol": "check_password",
        "chunk_type": "function",
        "start_line": 1,
        "end_line": 7,
        "content": """
def check_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password
    )
"""
    }
]


# ==========================================================
# CREATE VECTOR STORE
# ==========================================================

store = VectorStore()


# ==========================================================
# ADD CHUNKS
# ==========================================================

store.add_chunks(chunks)


# ==========================================================
# CHECK COUNT
# ==========================================================

print()
print("Number of stored chunks:", store.count())


# ==========================================================
# SEARCH
# ==========================================================

query = "Where is user authentication and login handled?"

results = store.search(
    query=query,
    limit=3
)


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print()
print("SEARCH RESULTS")
print("=" * 60)

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print("-" * 60)

    print("Score:", result.score)

    payload = result.payload

    print("File:", payload.get("file_path"))
    print("Symbol:", payload.get("symbol"))
    print("Type:", payload.get("chunk_type"))
    print(
        "Lines:",
        payload.get("start_line"),
        "-",
        payload.get("end_line")
    )

    print("\nCode:")
    print(payload.get("content"))
    store.close()