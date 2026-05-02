import html
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED_PATH = os.path.join(
    BASE_DIR,
    "Takeout",
    "Blogger",
    "Blogs",
    "Harish Vishwanath_s Diary",
    "feed.atom",
)
OUTPUT_DIR = os.path.join(BASE_DIR, "content", "posts")

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "blogger": "http://schemas.google.com/blogger/2018",
}


def sanitize_filename(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "post"


def parse_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def main():
    tree = ET.parse(FEED_PATH)
    root = tree.getroot()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    used_filenames = set()
    count = 0

    for entry in root.findall("atom:entry", NS):
        entry_type = entry.findtext("blogger:type", default="", namespaces=NS)
        if entry_type != "POST":
            continue

        title = entry.findtext("atom:title", default="", namespaces=NS).strip() or "Untitled"
        published = entry.findtext("atom:published", default="", namespaces=NS)
        updated = entry.findtext("atom:updated", default="", namespaces=NS)
        content = entry.findtext("atom:content", default="", namespaces=NS)
        filename = entry.findtext("blogger:filename", default="", namespaces=NS)

        tags = []
        for cat in entry.findall("atom:category", NS):
            term = cat.attrib.get("term", "").strip()
            if term and term != "None":
                tags.append(term)

        dt = parse_datetime(published)
        if not dt:
            continue

        slug_source = os.path.splitext(os.path.basename(filename))[0] or title
        slug = sanitize_filename(slug_source)
        date_prefix = dt.strftime("%Y-%m-%d")
        out_name = f"{date_prefix}-{slug}.md"

        while out_name in used_filenames:
            out_name = f"{date_prefix}-{slug}-{len(used_filenames)}.md"
        used_filenames.add(out_name)

        safe_title = title.replace("\"", "\\\"")
        front_matter = [
            "---",
            f"title: \"{safe_title}\"",
            f"date: {published}",
        ]
        if updated:
            front_matter.append(f"lastmod: {updated}")
        if tags:
            front_matter.append("tags:")
            front_matter.extend([f"  - {tag}" for tag in tags])
        if filename:
            front_matter.append(f"url: \"{filename}\"")
        front_matter.append("---")

        body = html.unescape(content or "")
        content_text = "\n".join(front_matter) + "\n\n" + body.strip() + "\n"

        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content_text)

        count += 1

    print(f"Imported {count} posts into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
