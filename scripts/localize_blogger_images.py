import imghdr
import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
ALBUM_DIR = ROOT / "Takeout" / "Blogger" / "Albums" / "Harish Vishwanath_s Diary"
OUT_DIR = ROOT / "static" / "images" / "blogger"
POSTS_DIR = ROOT / "content" / "posts"

GOOGLEUSER_RE = re.compile(r"https?://blogger\.googleusercontent\.com/[^)\s]+")
IMAGE_LINK_RE = re.compile(r"!\[([^\]]*)\]\((https?://blogger\.googleusercontent\.com/[^)\s]+)\)")
IMAGE_WRAP_RE = re.compile(
    r"\[!\[([^\]]*)\]\((https?://blogger\.googleusercontent\.com/[^)\s]+)\)\]\((https?://blogger\.googleusercontent\.com/[^)\s]+)\)"
)

EXT_MAP = {
    "jpeg": ".jpg",
    "png": ".png",
    "gif": ".gif",
}
VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".svg"}


def infer_ext(path: Path) -> str:
    if path.suffix and path.suffix.lower() in VALID_EXTS:
        return path.suffix
    kind = imghdr.what(path)
    if kind:
        return EXT_MAP.get(kind, "")
    with path.open("rb") as f:
        header = f.read(12)
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if header[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if header[:3] == b"\xff\xd8\xff":
        return ".jpg"
    return ""


def build_mapping():
    mapping = {}
    copied = {}

    for path in ALBUM_DIR.iterdir():
        if path.is_dir() or path.name.endswith(".json") or path.name == "metadata.json":
            continue
        ext = infer_ext(path)
        if not ext:
            continue
        name = path.name
        stem = path.stem
        dest_name = f"{stem}{ext}"
        dest_path = OUT_DIR / dest_name
        mapping[dest_name] = dest_name
        mapping[path.name] = dest_name
        mapping[f"{stem}{ext}"] = dest_name
        mapping[f"{path.name}{ext}"] = dest_name
        copied[dest_path] = path

    return mapping, copied


def decode_basename(base: str) -> str:
    last = base
    for _ in range(3):
        decoded = unquote(last)
        if decoded == last:
            break
        last = decoded
    return last


def map_url(url: str, mapping: dict) -> str:
    parsed = urlparse(url)
    base = os.path.basename(parsed.path)
    if not base:
        return url
    base = decode_basename(base)
    mapped = mapping.get(base)
    if not mapped:
        return url
    return f"/images/blogger/{mapped}"


def replace_urls(text: str, mapping: dict):
    def repl_wrapped(match):
        alt_text, thumb_url, full_url = match.groups()
        mapped_full = map_url(full_url, mapping)
        mapped_thumb = map_url(thumb_url, mapping)
        if mapped_thumb == thumb_url and mapped_full != full_url:
            mapped_thumb = mapped_full
        return f"[![{alt_text}]({mapped_thumb})]({mapped_full})"

    def repl_image(match):
        alt_text, img_url = match.groups()
        mapped = map_url(img_url, mapping)
        return f"![{alt_text}]({mapped})"

    text = IMAGE_WRAP_RE.sub(repl_wrapped, text)
    text = IMAGE_LINK_RE.sub(repl_image, text)
    return GOOGLEUSER_RE.sub(lambda m: map_url(m.group(0), mapping), text)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mapping, copied = build_mapping()

    for dest_path, src_path in copied.items():
        if not dest_path.exists():
            shutil.copy2(src_path, dest_path)

    updated = []
    for path in POSTS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        new_text = replace_urls(text, mapping)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated.append(path)

    print(f"Copied {len(copied)} images into {OUT_DIR}")
    print(f"Updated {len(updated)} posts")
    for path in updated:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
