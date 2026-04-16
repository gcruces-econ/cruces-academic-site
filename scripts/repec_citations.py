#!/usr/bin/env python3

import html
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0 Safari/537.36"
    )
}
MONTH_NAMES = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


class MetaTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta":
            return

        attr_map = {key.lower(): value for key, value in attrs}
        name = attr_map.get("name")
        content = attr_map.get("content")
        if not name or content is None:
            return

        self.meta.setdefault(name.lower(), html.unescape(content).strip())


def normalize_text(value):
    value = html.unescape(str(value or ""))
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def fetch_html(url):
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_meta_tags(html_text):
    parser = MetaTagParser()
    parser.feed(html_text)
    return parser.meta


def split_authors(author_field):
    if not author_field:
        return []

    if ";" in author_field:
        parts = author_field.split(";")
    else:
        parts = re.split(r"\s*&\s*", author_field)

    return [normalize_text(part) for part in parts if normalize_text(part)]


def format_given_initials(given_names):
    parts = []
    for token in given_names.split():
        token = token.strip().strip(".")
        if not token:
            continue

        hyphen_parts = [part for part in token.split("-") if part]
        if len(hyphen_parts) > 1:
            parts.append("-".join(f"{part[0].upper()}." for part in hyphen_parts))
        else:
            parts.append(f"{token[0].upper()}.")

    return " ".join(parts)


def format_apa_author(name):
    name = normalize_text(name)
    if not name:
        return ""

    if "," in name:
        family_name, given_names = [normalize_text(part) for part in name.split(",", 1)]
    else:
        tokens = name.split()
        if len(tokens) == 1:
            return tokens[0]
        family_name = tokens[-1]
        given_names = " ".join(tokens[:-1])

    initials = format_given_initials(given_names)
    if not initials:
        return family_name

    return f"{family_name}, {initials}"


def format_apa_authors(author_field):
    authors = [format_apa_author(name) for name in split_authors(author_field)]
    authors = [author for author in authors if author]

    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]}, & {authors[1]}"

    return ", ".join(authors[:-1]) + f", & {authors[-1]}"


def format_bibtex_authors(author_field):
    authors = split_authors(author_field)
    return " and ".join(authors)


def format_apa_date(meta, include_month=False):
    year = normalize_text(meta.get("citation_year"))
    publication_date = normalize_text(meta.get("citation_publication_date"))

    if not year and publication_date:
        match = re.match(r"(\d{4})", publication_date)
        if match:
            year = match.group(1)

    if not include_month or not publication_date:
        return year or "n.d."

    match = re.match(r"(\d{4})[-/](\d{2})", publication_date)
    if not match:
        return year or "n.d."

    month_name = MONTH_NAMES.get(match.group(2))
    if not month_name:
        return year or "n.d."

    return f"{match.group(1)}, {month_name}"


def extract_month(meta):
    publication_date = normalize_text(meta.get("citation_publication_date"))
    match = re.match(r"\d{4}[-/](\d{2})", publication_date)
    if not match:
        return ""

    return MONTH_NAMES.get(match.group(1), "")


def format_pages(meta):
    first_page = normalize_text(meta.get("citation_firstpage"))
    last_page = normalize_text(meta.get("citation_lastpage"))
    if first_page and last_page:
        return f"{first_page}-{last_page}"
    if first_page:
        return first_page
    return ""


def format_series_number(meta):
    number = normalize_text(meta.get("citation_technical_report_number"))
    if number:
        return number

    return normalize_text(meta.get("citation_report_number"))


def build_article_apa(meta, url):
    authors = format_apa_authors(meta.get("citation_authors"))
    date = format_apa_date(meta)
    title = normalize_text(meta.get("citation_title"))
    journal = normalize_text(meta.get("citation_journal_title"))
    volume = normalize_text(meta.get("citation_volume"))
    issue = normalize_text(meta.get("citation_issue"))
    pages = format_pages(meta)
    doi = normalize_text(meta.get("doi"))

    citation = f"{authors} ({date}). {title}."
    if journal:
        citation += f" {journal}"

    if volume:
        if issue and issue.upper() not in {"C", "NONE"}:
            citation += f", {volume}({issue})"
        else:
            citation += f", {volume}"

    if pages:
        citation += f", {pages}"

    citation += "."

    if doi:
        citation += f" https://doi.org/{doi}"
    elif url:
        citation += f" {url}"

    return citation.strip()


def build_paper_apa(meta, url):
    authors = format_apa_authors(meta.get("citation_authors"))
    date = format_apa_date(meta, include_month=True)
    title = normalize_text(meta.get("citation_title"))
    series_name = normalize_text(meta.get("citation_journal_title"))
    number = format_series_number(meta)
    publisher = normalize_text(meta.get("citation_publisher"))

    citation = f"{authors} ({date}). {title}."

    if series_name and number:
        citation += f" ({series_name} No. {number})."
    elif series_name:
        citation += f" ({series_name})."

    if publisher:
        citation += f" {publisher}."

    if url:
        citation += f" {url}"

    return citation.strip()


def build_generic_apa(meta, url):
    authors = format_apa_authors(meta.get("citation_authors"))
    date = format_apa_date(meta, include_month=True)
    title = normalize_text(meta.get("citation_title"))
    publisher = normalize_text(meta.get("citation_publisher"))

    citation = f"{authors} ({date}). {title}."
    if publisher:
        citation += f" {publisher}."
    if url:
        citation += f" {url}"

    return citation.strip()


def bibtex_escape(value):
    value = normalize_text(value)
    value = value.replace("\\", "\\\\")
    value = value.replace("{", "\\{").replace("}", "\\}")
    return value


def build_bibtex_fields(meta, url):
    fields = []

    def add_field(name, value):
        value = bibtex_escape(value)
        if value and value.upper() != "NONE":
            fields.append((name, value))

    add_field("author", format_bibtex_authors(meta.get("citation_authors")))
    add_field("title", meta.get("citation_title"))
    add_field("year", meta.get("citation_year"))
    add_field("month", extract_month(meta))
    add_field("abstract", meta.get("citation_abstract"))
    add_field("keywords", meta.get("citation_keywords"))
    add_field("doi", meta.get("doi"))
    add_field("url", url)

    citation_type = normalize_text(meta.get("citation_type")).lower()
    if citation_type == "redif-article":
        add_field("journal", meta.get("citation_journal_title"))
        add_field("volume", meta.get("citation_volume"))
        issue = normalize_text(meta.get("citation_issue"))
        if issue.upper() not in {"C", "NONE"}:
            add_field("number", issue)
        add_field("pages", format_pages(meta))
    elif citation_type == "redif-paper":
        add_field("institution", meta.get("citation_publisher"))
        add_field("series", meta.get("citation_journal_title"))
        add_field("number", format_series_number(meta))
    else:
        add_field("publisher", meta.get("citation_publisher"))

    return fields


def build_bibtex_citation(meta, url, handle):
    citation_type = normalize_text(meta.get("citation_type")).lower()
    if citation_type == "redif-article":
        entry_type = "Article"
    elif citation_type == "redif-paper":
        entry_type = "TechReport"
    else:
        entry_type = "Misc"

    key = normalize_text(handle).lower()
    fields = build_bibtex_fields(meta, url)
    lines = [f"@{entry_type}{{{key},"]

    for name, value in fields:
        lines.append(f"{name}={{{value}}},")

    lines.append("}")
    return "\n".join(lines)


def build_apa_citation(meta, url):
    citation_type = normalize_text(meta.get("citation_type")).lower()

    if citation_type == "redif-article":
        return build_article_apa(meta, url)
    if citation_type == "redif-paper":
        return build_paper_apa(meta, url)

    return build_generic_apa(meta, url)


def extract_citation_bundle(url):
    html_text = fetch_html(url)
    meta = parse_meta_tags(html_text)
    handle = normalize_text(meta.get("handle"))
    if not handle:
        raise ValueError(f"Missing RePEc handle for {url}")

    apa = build_apa_citation(meta, url)
    bibtex = build_bibtex_citation(meta, url, handle)

    if not apa:
        raise ValueError(f"Missing APA citation for {url}")
    if not bibtex:
        raise ValueError(f"Missing BibTeX citation for {url}")

    return {
        "citationApa": apa,
        "citationBibtex": bibtex,
    }


def load_cached_citations(site_data_path):
    path = Path(site_data_path)
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}

    cached = {}
    for section in ("selectedPapers", "workingPapers"):
        for item in data.get(section, []):
            url = item.get("url")
            citation_apa = normalize_text(item.get("citationApa"))
            citation_bibtex = str(item.get("citationBibtex", "")).strip()
            if url and citation_apa and citation_bibtex:
                cached[url] = {
                    "citationApa": citation_apa,
                    "citationBibtex": citation_bibtex,
                }

    return cached


def attach_citations(items, cached_citations, label, refresh=False):
    total = len(items)
    missing_count = 0

    for index, item in enumerate(items, start=1):
        url = item.get("url")
        if not url:
            continue

        citations = None if refresh else cached_citations.get(url)
        if not citations:
            try:
                citations = extract_citation_bundle(url)
            except Exception:
                missing_count += 1
                citations = None

        if citations:
            cached_citations[url] = citations
            item.update(citations)

        if index % 10 == 0 or index == total:
            print(f"{label}: {index}/{total}")

    if missing_count:
        print(f"{label}: {missing_count} items without citation data")
