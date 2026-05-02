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


def format_poem(body: str) -> str:
    lines = [line.rstrip() for line in body.splitlines()]
    if not lines:
        return body

    # Preserve leading/trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    # If there are stanza breaks beyond the title line, keep as-is.
    tail_lines = lines[2:] if len(lines) > 2 else []
    if any(not line.strip() for line in tail_lines):
        return body

    date_line = None
    if lines and DATE_RE.match(lines[-1].strip()):
        date_line = lines.pop()

    stanzas = []
    stanza = []
    for line in lines:
        stanza.append(line)
        if len(stanza) == 4:
            stanzas.append(stanza)
            stanza = []
    if stanza:
        stanzas.append(stanza)

    output_lines = []
    for idx, stanza in enumerate(stanzas):
        output_lines.extend(stanza)
        if idx != len(stanzas) - 1:
            output_lines.append("")

    if date_line:
        output_lines.append("")
        output_lines.append(date_line)

    return "\n".join(output_lines) + "\n"


def main():
    changed = []
    for path in POSTS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not has_poetry_tag(text):
            continue
        front, body = split_front_matter(text)
        if not front:
            continue
        new_body = format_poem(body)
        if new_body != body:
            new_text = front + "\n" + new_body
            path.write_text(new_text, encoding="utf-8")
            changed.append(path)

    print(f"Updated {len(changed)} poems")
    for path in changed:
        print(path.name)


if __name__ == "__main__":
    main()
