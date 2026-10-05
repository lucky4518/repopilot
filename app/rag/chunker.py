
import ast


def make_chunk(
    content: str,
    file_path: str,
    language: str,
    symbol: str,
    chunk_type: str,
    start_line: int,
    end_line: int,
) -> dict:
    return {
        "content": content,
        "metadata": {
            "file_path": file_path,
            "language": language,
            "symbol": symbol,
            "chunk_type": chunk_type,
            "start_line": start_line,
            "end_line": end_line,
        },
    }


def chunk_python(file_record: dict) -> list[dict]:
    source = file_record["content"]
    file_path = file_record["file_path"]
    lines = source.splitlines()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Invalid or unsupported Python syntax.
        return chunk_by_lines(file_record)

    chunks = []

    def visit(node, parent_name=""):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef,
                                  ast.AsyncFunctionDef)):
                name = (
                    f"{parent_name}.{child.name}"
                    if parent_name
                    else child.name
                )

                start = child.lineno
                end = child.end_lineno

                content = "\n".join(lines[start - 1:end])

                chunks.append(
                    make_chunk(
                        content=content,
                        file_path=file_path,
                        language="python",
                        symbol=name,
                        chunk_type=(
                            "method" if parent_name else "function"
                        ),
                        start_line=start,
                        end_line=end,
                    )
                )

                # Include nested functions, if any.
                visit(child, name)

            elif isinstance(child, ast.ClassDef):
                start = child.lineno
                end = child.end_lineno

                content = "\n".join(lines[start - 1:end])

                chunks.append(
                    make_chunk(
                        content=content,
                        file_path=file_path,
                        language="python",
                        symbol=child.name,
                        chunk_type="class",
                        start_line=start,
                        end_line=end,
                    )
                )

                visit(child, child.name)

    visit(tree)

    # Preserve imports, constants and other file-level code.
    covered = set()

    for chunk in chunks:
        metadata = chunk["metadata"]
        covered.update(
            range(
                metadata["start_line"],
                metadata["end_line"] + 1,
            )
        )

    remaining = [
        (i, line)
        for i, line in enumerate(lines, start=1)
        if i not in covered and line.strip()
    ]

    if remaining:
        content = "\n".join(line for _, line in remaining)

        chunks.append(
            make_chunk(
                content=content,
                file_path=file_path,
                language="python",
                symbol="<module>",
                chunk_type="module",
                start_line=remaining[0][0],
                end_line=remaining[-1][0],
            )
        )

    return chunks


def chunk_by_lines(
    file_record: dict,
    max_lines: int = 80,
    overlap: int = 10,
) -> list[dict]:
    lines = file_record["content"].splitlines()
    chunks = []

    if not lines:
        return chunks

    step = max_lines - overlap
    start = 0

    while start < len(lines):
        end = min(start + max_lines, len(lines))

        chunks.append(
            make_chunk(
                content="\n".join(lines[start:end]),
                file_path=file_record["file_path"],
                language=file_record["language"],
                symbol="<file>",
                chunk_type="text",
                start_line=start + 1,
                end_line=end,
            )
        )

        if end == len(lines):
            break

        start += step

    return chunks


def chunk_file(file_record: dict) -> list[dict]:
    if file_record["language"] == "py":
        return chunk_python(file_record)

    return chunk_by_lines(file_record)


def chunk_repository(files: list[dict]) -> list[dict]:
    chunks = []

    for file_record in files:
        chunks.extend(chunk_file(file_record))

    return chunks