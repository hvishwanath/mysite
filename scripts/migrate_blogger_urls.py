from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"


def split_front_matter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            front = lines[: i + 1]
            body = lines[i + 1 :]
            return front, body
    return None, text


def parse_front_matter(lines):
    data = {}
    current_key = None
    for line in lines[1:-1]:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(line.replace("  - ", "", 1))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
            current_key = key.strip()
    return data


def build_front_matter(data):
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return lines


def main():
    updated = []
    for path in POSTS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        front, body = split_front_matter(text)
        if not front:
            continue
        data = parse_front_matter(front)
        url = data.pop("url", None)
        if not url:
            continue
        url = url.strip().strip("\"")
        if url:
            aliases = data.get("aliases", [])
            if isinstance(aliases, str):
                aliases = [aliases]
            if url not in aliases:
                aliases.append(url)
            data["aliases"] = aliases

        new_front = build_front_matter(data)
        new_text = "\n".join(new_front) + "\n" + "\n".join(body).lstrip("\n")
        path.write_text(new_text, encoding="utf-8")
        updated.append(path)

    print(f"Updated {len(updated)} posts")


if __name__ == "__main__":
    main()
