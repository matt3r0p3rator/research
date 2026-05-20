#!/usr/bin/env python3
"""
Import all research markdown files into Trilium via ETAPI (one note at a time).
Usage: ETAPI_TOKEN=<token> python3 import_to_trilium.py
"""

import os
import re
import sys
import markdown as md_lib
import requests

TRILIUM_URL = os.environ.get("TRILIUM_URL", "http://localhost:8023")
ETAPI_TOKEN = os.environ.get("ETAPI_TOKEN", "")
PARENT_NOTE_ID = os.environ.get("PARENT_NOTE_ID", "root")

RESEARCH_DIRS = [
    "charts",
    "cloud-chamber",
    "crypto",
    "private-maritime",
    "refrigeration",
    "school-search",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# ETAPI helpers
# ---------------------------------------------------------------------------

def api(method: str, path: str, **kwargs):
    url = f"{TRILIUM_URL}/etapi{path}"
    headers = {"Authorization": ETAPI_TOKEN, "Content-Type": "application/json"}
    resp = getattr(requests, method)(url, headers=headers, timeout=30, **kwargs)
    if resp.status_code not in (200, 201, 204):
        print(f"  ERROR {resp.status_code}: {resp.text}", file=sys.stderr)
        resp.raise_for_status()
    return resp.json() if resp.content else {}


def create_note(parent_id: str, title: str, note_type: str, content: str) -> str:
    result = api("post", "/create-note", json={
        "parentNoteId": parent_id,
        "title": title,
        "type": note_type,
        "content": content,
    })
    return result["note"]["noteId"]


def update_note_content(note_id: str, html: str) -> None:
    # Ensure there is always some string content, Trilium rejects empty/null content
    if not html or not html.strip():
        html = "<p></p>"
    url = f"{TRILIUM_URL}/etapi/notes/{note_id}/content"
    # Content body must be sent as raw string data or with content-type text/plain or text/html
    # Some Trilium ETAPI versions prefer string payload on the content endpoint
    headers = {"Authorization": ETAPI_TOKEN, "Content-Type": "text/plain"}
    resp = requests.put(url, headers=headers, data=html.encode("utf-8"), timeout=30)
    if resp.status_code not in (200, 201, 204):
        print(f"  ERROR {resp.status_code}: {resp.text}", file=sys.stderr)
        resp.raise_for_status()


# ---------------------------------------------------------------------------
# Markdown → Trilium HTML conversion
# ---------------------------------------------------------------------------

def md_to_html(raw: str, file_rel_dir: str = "", path_to_id: dict | None = None) -> str:
    """Convert markdown to Trilium-compatible HTML.

    If file_rel_dir and path_to_id are supplied, relative .md links are
    resolved to Trilium reference links using the note-ID map.
    """
    placeholders: dict[str, str] = {}

    def stash(html: str) -> str:
        key = f"TRILIUMSTASH{len(placeholders)}END"
        placeholders[key] = html
        return key

    # Stash inter-note .md links BEFORE markdown sees them
    if path_to_id is not None:
        def replace_md_link(m: re.Match) -> str:
            text = m.group(1)
            href = m.group(2)
            href_path = href.split("#")[0]
            if not href_path.endswith(".md"):
                return m.group(0)
            abs_path = os.path.normpath(os.path.join(BASE_DIR, file_rel_dir, href_path))
            rel = os.path.relpath(abs_path, BASE_DIR)
            note_id = path_to_id.get(rel)
            if note_id:
                return stash(f'<a class="reference-link" href="#{note_id}">{text}</a>')
            return m.group(0)

        raw = re.sub(r"\[([^\]]*)\]\(([^)]+)\)", replace_md_link, raw)

    # Block math $$...$$ → KaTeX block span (before inline to avoid double-match)
    raw = re.sub(
        r"\$\$(.+?)\$\$",
        lambda m: stash(f'<span class="math-tex">\\[{m.group(1).strip()}\\]</span>'),
        raw, flags=re.DOTALL,
    )
    # Inline math $...$
    raw = re.sub(
        r"\$([^\$\n]+?)\$",
        lambda m: stash(f'<span class="math-tex">\\({m.group(1).strip()}\\)</span>'),
        raw,
    )

    html = md_lib.markdown(raw, extensions=["tables", "fenced_code", "toc"])

    # Restore all stashed HTML
    for key, value in placeholders.items():
        html = html.replace(key, value)

    # Wrap <table> for CKEditor (requires <figure class="table"> container)
    html = re.sub(r"<table>", '<figure class="table"><table>', html)
    html = re.sub(r"</table>", "</table></figure>", html)

    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not ETAPI_TOKEN:
        print("Error: set ETAPI_TOKEN environment variable first.", file=sys.stderr)
        print("  In Trilium: Options → ETAPI → Generate new token", file=sys.stderr)
        sys.exit(1)

    # Pass 1: create all notes, record path → noteId
    path_to_id: dict[str, str] = {}   # relative path from BASE_DIR → noteId
    note_files: list[tuple[str, str, str]] = []  # (rel_dir, fname, noteId)

    print("Pass 1: creating notes...")
    for folder in RESEARCH_DIRS:
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.isdir(folder_path):
            print(f"  [skip] {folder}/ not found")
            continue

        md_files = sorted(f for f in os.listdir(folder_path) if f.endswith(".md"))
        if not md_files:
            continue

        folder_id = create_note(PARENT_NOTE_ID, folder.replace("-", " ").title(), "book", "")
        print(f"  [folder] {folder} ({folder_id})")

        for fname in md_files:
            title = fname[:-3].replace("-", " ").title()
            raw = open(os.path.join(folder_path, fname), encoding="utf-8").read()
            html = md_to_html(raw)  # pass 1: no link IDs yet
            note_id = create_note(folder_id, title, "text", html)
            rel_path = os.path.join(folder, fname)
            path_to_id[rel_path] = note_id
            note_files.append((folder, fname, note_id))
            print(f"    + {fname} → {note_id}")

    # Pass 2: re-render with resolved note links and update content
    print("\nPass 2: fixing inter-note links...")
    fixed = 0
    for rel_dir, fname, note_id in note_files:
        raw = open(os.path.join(BASE_DIR, rel_dir, fname), encoding="utf-8").read()
        html = md_to_html(raw, rel_dir, path_to_id)
        update_note_content(note_id, html)
        fixed += 1

    print(f"\nDone — {fixed} notes imported and linked.")


if __name__ == "__main__":
    main()

