import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"

FENCE_RE = re.compile(r"^```")
LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)")
BLOCK_RE = re.compile(r"^\s*(?:#|>|!\[|\[!\[)")


def split_front_matter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            front = "\n".join(lines[: i + 1])
            body = "\n".join(lines[i + 1 :])
            return front, body
    return None, text


def has_poetry_tag(text: str) -> bool:
    return bool(re.search(r"^tags:\n(?:  - .+\n)*  - poetry\n", text, re.M))


def is_block_line(line: str) -> bool:
    if not line.strip():
        return True
    if FENCE_RE.match(line):
        return True
    if LIST_RE.match(line):
        return True
    if BLOCK_RE.match(line):
        return True
    if line.strip().startswith("{{<"):
        return True
    if "|" in line and line.strip().startswith("|"):
        return True
    return False


def unwrap_body(body: str) -> str:
    lines = body.splitlines()
    out = []
    buffer = []
    in_code = False

    def flush_buffer():
        nonlocal buffer
        if buffer:
            joined = " ".join(line.strip() for line in buffer)
            out.append(joined)
            buffer = []

    for line in lines:
        if FENCE_RE.match(line):
            flush_buffer()
            out.append(line)
            in_code = not in_code
            continue

        if in_code:
            out.append(line)
            continue

        if not line.strip():
            flush_buffer()
            out.append("")
            continue

        if is_block_line(line):
            flush_buffer()
            out.append(line.rstrip())
            continue

        buffer.append(line)

    flush_buffer()
    return "\n".join(out).rstrip() + "\n"


def main():
    changed = []
    for path in POSTS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if has_poetry_tag(text):
            continue
        front, body = split_front_matter(text)
        if not front:
            continue
        new_body = unwrap_body(body)
        if new_body != body:
            path.write_text(front + "\n" + new_body, encoding="utf-8")
            changed.append(path)

    print(f"Updated {len(changed)} posts")
    for path in changed:
        print(path.name)


if __name__ == "__main__":
    main()
