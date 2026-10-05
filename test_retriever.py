from app.rag.search import CodeSearch


# ==========================================================
# SAMPLE REPOSITORY CHUNKS
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
# CREATE SEARCH ENGINE
# ==========================================================

search_engine = CodeSearch(chunks)


# ==========================================================
# USER QUERY
# ==========================================================

query = "Where is authentication and login handled?"


# ==========================================================
# SEARCH
# ==========================================================

results = search_engine.search(
    query=query,
    top_k=3
)


# ==========================================================
# DISPLAY
# ==========================================================

print()
print("QUERY:")
print(query)

print()
print("=" * 70)
print("RETRIEVED CODE")
print("=" * 70)


for i, result in enumerate(results, start=1):

    print()
    print(f"RESULT {i}")
    print("-" * 70)

    print("Score:", result["score"])

    print(
        "File:",
        result["file_path"]
    )

    print(
        "Symbol:",
        result["symbol"]
    )

    print(
        "Lines:",
        result["start_line"],
        "-",
        result["end_line"]
    )

    print()
    print(result["content"])