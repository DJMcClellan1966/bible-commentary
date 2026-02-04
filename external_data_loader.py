"""
Load and expose content from external reference data:
- Catholic Encyclopedia (cathen)
- Church Fathers (fathers)
- Summa Theologica (summa)
- Douay-Rheims (douay) and library as needed

Data path is set in config.EXTERNAL_DATA_ROOT (default: ../bible-commentary/data).
"""
import os
import re
import html
from typing import Optional, Dict, List, Tuple

try:
    from config import EXTERNAL_DATA_ROOT
except ImportError:
    EXTERNAL_DATA_ROOT = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "bible-commentary", "data")
    )


COLLECTIONS = ("cathen", "fathers", "summa", "douay", "library")
SOURCE_LABELS = {
    "cathen": "Catholic Encyclopedia",
    "fathers": "Church Fathers",
    "summa": "Summa Theologica",
    "douay": "Douay-Rheims",
    "library": "Library",
}


def _data_path(*parts: str) -> str:
    return os.path.join(EXTERNAL_DATA_ROOT, *parts)


def _is_available() -> bool:
    return os.path.isdir(EXTERNAL_DATA_ROOT)


def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def _strip_tags(html_fragment: str) -> str:
    # Remove script/style
    html_fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_fragment, flags=re.DOTALL | re.I)
    # Replace <br>, <p>, etc. with newline
    html_fragment = re.sub(r"<br\s*/?>", "\n", html_fragment, flags=re.I)
    html_fragment = re.sub(r"</p>", "\n", html_fragment, flags=re.I)
    html_fragment = re.sub(r"</(div|h[1-6]|li|blockquote)>", "\n", html_fragment, flags=re.I)
    # Remove all remaining tags
    html_fragment = re.sub(r"<[^>]+>", " ", html_fragment)
    # Decode entities
    html_fragment = html.unescape(html_fragment)
    # Normalize whitespace
    html_fragment = re.sub(r"[ \t]+", " ", html_fragment)
    html_fragment = re.sub(r"\n\s*\n", "\n\n", html_fragment)
    return html_fragment.strip()


def _extract_title(raw: str) -> str:
    # From <title>...</title>
    m = re.search(r"<title[^>]*>([^<]+)</title>", raw, re.I)
    if m:
        title = html.unescape(m.group(1).strip())
        # Remove source prefix like "CATHOLIC ENCYCLOPEDIA: " or "CHURCH FATHERS: "
        for prefix in ("CATHOLIC ENCYCLOPEDIA:", "CHURCH FATHERS:", "SUMMA THEOLOGICA:"):
            if title.upper().startswith(prefix):
                title = title[len(prefix) :].strip()
                break
        return title
    # From first <h1>
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", raw, re.I)
    if m:
        return html.unescape(m.group(1).strip())
    return ""


def _extract_body(raw: str) -> str:
    # Content inside <div id="springfield2"> ... </div>
    m = re.search(r"<div\s+id=[\"']springfield2[\"'][^>]*>(.*?)</div>\s*<div", raw, re.DOTALL | re.I)
    if m:
        return _strip_tags(m.group(1))
    # Fallback: everything between first <h1> and footer/end
    m = re.search(r"<h1[^>]*>.*?</h1>\s*(.*?)(?:<div\s+id=[\"']ogdenville|</body>)", raw, re.DOTALL | re.I)
    if m:
        return _strip_tags(m.group(1))
    return _strip_tags(raw)


def get_article(collection: str, path_or_id: str) -> Optional[Dict]:
    """
    Load one article by collection and filename (e.g. '00001a.htm') or path.
    Returns { "title", "text", "source", "collection" } or None if not found.
    """
    if collection not in COLLECTIONS:
        return None
    if not _is_available():
        return None
    # Normalize: no path traversal, only basename if it looks like a file
    base = os.path.basename(path_or_id)
    if not base.endswith(".htm") and not base.endswith(".html"):
        base = path_or_id if path_or_id.endswith((".htm", ".html")) else path_or_id + ".htm"
    path = _data_path(collection, base)
    if not os.path.isfile(path):
        return None
    raw = _read_file(path)
    if not raw:
        return None
    return {
        "title": _extract_title(raw),
        "text": _extract_body(raw),
        "source": SOURCE_LABELS.get(collection, collection),
        "collection": collection,
        "id": base,
    }


def list_entries(
    collection: str, prefix: str = "", limit: int = 100
) -> List[Dict]:
    """
    List entries (filename + title) for a collection, optionally filtered by prefix.
    prefix can be a letter (e.g. 'a') or filename prefix.
    """
    if collection not in COLLECTIONS:
        return []
    if not _is_available():
        return []
    dir_path = _data_path(collection)
    if not os.path.isdir(dir_path):
        return []
    entries = []
    prefix_lower = (prefix or "").strip().lower()
    for name in sorted(os.listdir(dir_path)):
        if not name.endswith((".htm", ".html")):
            continue
        path = os.path.join(dir_path, name)
        if not os.path.isfile(path):
            continue
        raw = _read_file(path)
        title = _extract_title(raw) if raw else name
        if prefix_lower:
            if not name.lower().startswith(prefix_lower) and not (title and title.lower().startswith(prefix_lower)):
                continue
        if len(entries) >= limit:
            break
        entries.append({"id": name, "title": title})
    return entries


def search_titles(collection: str, q: str, limit: int = 30) -> List[Dict]:
    """Simple title search (substring)."""
    if not q or not q.strip():
        return list_entries(collection, limit=limit)
    q = q.strip().lower()
    all_entries = list_entries(collection, limit=500)
    return [e for e in all_entries if q in (e.get("title") or "").lower()][:limit]


def get_availability() -> Dict[str, bool]:
    """Report which collections have data available."""
    return {
        c: os.path.isdir(_data_path(c))
        for c in COLLECTIONS
    }
