import re
from pathlib import Path

import html2text

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"

FENCE_RE = re.compile(r"```.*?```", re.S)
HTML_RE = re.compile(r"<[/a-zA-Z][^>]*>")


def split_front_matter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            front = "\n".join(lines[: i + 1])
            body = "\n".join(lines[i + 1 :])
            return front, body
    return "", text


def protect_fences(text: str):
    blocks = []

    def repl(match):
        blocks.append(match.group(0))
        return f"@@CODEBLOCK{len(blocks) - 1}@@"

    return FENCE_RE.sub(repl, text), blocks


def restore_fences(text: str, blocks):
    for i, block in enumerate(blocks):
        text = text.replace(f"@@CODEBLOCK{i}@@", block)
    return text


def convert_body(body: str):
    if not HTML_RE.search(body):
        return body

    protected, blocks = protect_fences(body)

    h = html2text.HTML2Text()
    h.body_width = 0
    h.single_line_break = True
    h.ignore_images = False
    h.ignore_links = False
    h.ignore_emphasis = False

    converted = h.handle(protected)
    converted = restore_fences(converted, blocks)

    cleaned_lines = [line.rstrip() for line in converted.splitlines()]
    return "\n".join(cleaned_lines).strip() + "\n"


def main():
    changed = []
    for path in POSTS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        front, body = split_front_matter(text)
        new_body = convert_body(body)
        if new_body != body:
            new_text = front + "\n" + new_body if front else new_body
            path.write_text(new_text, encoding="utf-8")
            changed.append(path)

    print(f"Converted {len(changed)} files")
    for path in changed:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
