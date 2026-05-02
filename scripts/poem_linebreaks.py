import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"

DATE_RE = re.compile(r"^\d{1,2}\s+[A-Z]{3}\s+\d{4}$")


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


def add_line_breaks(body: str) -> str:
    lines = body.splitlines()
    if not lines:
        return body

    # find first non-empty line as poem title
    title_idx = None
    for i, line in enumerate(lines):
        if line.strip():
            title_idx = i
            break

    out = []
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if not stripped:
            out.append("")
            continue
        if title_idx is not None and i == title_idx:
            out.append(stripped)
            continue
        if DATE_RE.match(stripped):
            out.append(stripped)
            continue
        if not stripped.endswith("  "):
            stripped = stripped + "  "
        out.append(stripped)

    return "\n".join(out) + "\n"


def main():
    changed = []
    for path in POSTS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not has_poetry_tag(text):
            continue
        front, body = split_front_matter(text)
        if not front:
            continue
        new_body = add_line_breaks(body)
        if new_body != body:
            path.write_text(front + "\n" + new_body, encoding="utf-8")
            changed.append(path)

    print(f"Updated {len(changed)} poems")
    for path in changed:
        print(path.name)


if __name__ == "__main__":
    main()
