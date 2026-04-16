#!/usr/bin/env python3

from pathlib import Path

import yaml

from repec_citations import attach_citations, load_cached_citations


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = REPO_ROOT / "site" / "content"
SITE_DATA_PATH = REPO_ROOT / "site" / "data" / "site-data.json"
SECTION_FILES = {
    "Published papers": CONTENT_ROOT / "published-papers.yml",
    "Working papers": CONTENT_ROOT / "working-papers.yml",
}


def load_items(path):
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, list):
        raise TypeError(f"{path} must contain a YAML list")

    return data


def write_items(path, items):
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(
            items,
            handle,
            sort_keys=False,
            allow_unicode=True,
            width=1000,
        )


def main():
    cached_citations = load_cached_citations(SITE_DATA_PATH)

    for label, path in SECTION_FILES.items():
        items = load_items(path)
        attach_citations(items, cached_citations, label)
        write_items(path, items)
        print(f"Updated {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
