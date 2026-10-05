
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py", ".cpp", ".cc", ".c", ".h", ".hpp",
    ".js", ".jsx", ".ts", ".tsx",
    ".java", ".go", ".rs",
    ".md", ".txt", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".sql",
}

IGNORED_DIRECTORIES = {
    ".git", ".venv", "venv", "node_modules",
    "__pycache__", ".pytest_cache",
    "dist", "build", ".next", "vendor",
}

MAX_FILE_SIZE = 500_000  # 500 KB


def load_repository(repo_path: str) -> list[dict]:
    root = Path(repo_path).resolve()

    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid repository directory: {root}")

    files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        # Skip files inside ignored directories.
        relative_path = path.relative_to(root)

        if any(part in IGNORED_DIRECTORIES
               for part in relative_path.parts):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                continue

            content = path.read_text(encoding="utf-8")

        except (OSError, UnicodeDecodeError):
            continue

        if not content.strip():
            continue

        files.append({
            "file_path": relative_path.as_posix(),
            "absolute_path": str(path),
            "content": content,
            "language": path.suffix.lower().lstrip("."),
        })

    return files