#!/usr/bin/env python3

import json
import re
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
import yaml
from repec_citations import attach_citations, load_cached_citations

IDEAS_AUTHOR_URL = "https://ideas.repec.org/e/pcr20.html"
IDEAS_BASE_URL = "https://ideas.repec.org"
OUTPUT_PATH = "site/data/site-data.json"
CONTENT_DIR = Path("site/content")
BUILD_SCRIPT = Path("scripts/build_site_content.py")
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0 Safari/537.36"
    )
}

PROFILE_LINKS = [
    {
        "title": "Current CV",
        "description": "Current curriculum vitae.",
        "url": "https://www.dropbox.com/s/u88tuj8n3hh9asl/CV_CRUCES_2023_EN_Web.pdf?dl=0",
        "linkLabel": "Open PDF",
    },
    {
        "title": "Email",
        "description": "Primary contact email.",
        "url": "mailto:gcruces@cedlas.org",
        "linkLabel": "Write email",
    },
    {
        "title": "Google Scholar",
        "description": "Citation profile and indexed publications.",
        "url": "https://scholar.google.com/citations?user=CylXqSUAAAAJ&hl=en",
        "linkLabel": "Open profile",
    },
    {
        "title": "Publications page",
        "description": "Full publication archive and paper records.",
        "url": "https://ideas.repec.org/e/pcr20.html",
        "linkLabel": "Open page",
    },
    {
        "title": "SSRN",
        "description": "Social Science Research Network author page.",
        "url": "http://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=651651",
        "linkLabel": "Open profile",
    },
    {
        "title": "Nottingham profile",
        "description": "University of Nottingham School of Economics faculty page.",
        "url": "https://www.nottingham.ac.uk/economics/people/guillermo.cruces",
        "linkLabel": "Open page",
    },
    {
        "title": "Nottingham School of Economics",
        "description": "Department page.",
        "url": "https://www.nottingham.ac.uk/economics/",
        "linkLabel": "Open site",
    },
    {
        "title": "IZA",
        "description": "IZA profile.",
        "url": "http://www.iza.org/en/webcontent/personnel/photos/index_html?key=2723",
        "linkLabel": "Open profile",
    },
]

ONGOING_PROJECTS = [
    {
        "title": "Paradoxical polarization and vaccine hesitancy in the USA",
        "status": "Under analysis",
        "description": "Joint work with Andy Brownback, Silvia Sonderegger, Seung-Keun Martinez, and Ignacio Lunghi.",
    },
    {
        "title": "Prices and preferences for tobacco and e-cigarette products in Argentina",
        "status": "Data collected",
        "description": "Joint work with Julieta Puig and Camila Campiti.",
    },
    {
        "title": "Tax compliance and mystery shopper random audits in Slovakia",
        "status": "Ongoing RCT",
        "description": "With Robert Priesol and Shafik Hebous.",
    },
    {
        "title": "Shifting merits: gender disparities in achievement recognition",
        "status": "Ongoing RCT",
        "description": "With Camila Campiti and Julieta Cabral.",
    },
    {
        "title": "Low Take-Up of Benefits",
        "status": "PEP Network project",
        "description": "Field-experiment evidence from beneficiaries of Argentina's conditional cash transfers.",
    },
]

POLICY_PUBLICATIONS = [
    {
        "title": "Time for a New Course: An Essay on Social Protection and Growth in Latin America",
        "year": "2021",
        "description": "A broad policy essay with Santiago Levy on social protection, growth, and institutional design in Latin America.",
        "file": "CRUCES LEVY 2022 undp-rblac-PNUD_bckPapers24-OK.pdf",
    },
    {
        "title": "Growth, Employment, and Poverty in Latin America",
        "year": "2017",
        "description": "Book-length treatment of inclusive growth, labor markets, and poverty reduction with Gary Fields, David Jaume, and Mariana Viollaz.",
        "file": "Book Cruces Fields Jaume Viollaz 2017 OUP WIDER.pdf",
    },
    {
        "title": "Inequality in Education. Evidence for Latin America",
        "year": "2014",
        "description": "A chapter with C. Garcia Domench and Leonardo Gasparini on educational inequality across the region.",
        "file": "Cruces Garcia-Domench Gasparini Falling Inequality Chapter 15 OUP 2013.pdf",
    },
    {
        "title": "Labor Informality and the Incentive Effects of Social Protection Systems",
        "year": "2014",
        "description": "A book chapter version of work on labor informality and health reform in Uruguay, coauthored with Marcelo Bergolo.",
        "file": "Bergolo Cruces IZA proof chapter4.pdf",
    },
    {
        "title": "A Distribution in Motion: The Case of Argentina",
        "year": "2010",
        "description": "An overview of inequality dynamics in Argentina with Leonardo Gasparini, bridging empirical evidence and policy debates.",
        "file": "Gasparini Cruces Distribution in motion Argentina doc_cedlas 78 2008.pdf",
    },
    {
        "title": "Los programas sociales en Argentina hacia el Bicentenario",
        "year": "2008",
        "description": "Co-edited volume on social programs in Argentina, with accompanying introductory and chapter materials in the archive.",
        "file": "Los programas sociales en Argentina BAJA.pdf",
    },
]

RESOURCES = [
    {
        "title": "Local CV document",
        "description": "The repo's local CV working file used during the Google Site migration.",
        "file": "CV_CRUCES_2026_EN.doc",
        "linkLabel": "Open file",
    },
    {
        "title": "Selected publications PDF",
        "description": "Legacy compiled publication list from the local archive.",
        "file": "publicaciones.pdf",
        "linkLabel": "Open file",
    },
    {
        "title": "CONICET publications list",
        "description": "Additional archive PDF with a broader compiled list of publications.",
        "file": "CONICET publicaciones.pdf",
        "linkLabel": "Open file",
    },
    {
        "title": "Historic archive bundle",
        "description": "ZIP archive containing earlier publication materials and related files.",
        "file": "publicaciones.zip",
        "linkLabel": "Open file",
    },
]


def normalize_text(value):
    value = value.replace("\xa0", " ")
    value = value.replace(" ,", ",")
    value = re.sub(r"\s+", " ", value)
    value = value.strip()

    if "Ã" in value or "â" in value:
        try:
            repaired = value.encode("latin-1").decode("utf-8")
        except UnicodeError:
            return value

        if repaired.count("Ã") + repaired.count("â") < value.count("Ã") + value.count("â"):
            value = repaired

    value = re.sub(
        r"(?:repec:[^\s]+\s+is not listed on IDEAS\s*)+",
        "",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"\bis not listed on IDEAS\b", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def fetch_html(url):
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def extract_abstract(url):
    soup = BeautifulSoup(fetch_html(url), "lxml")
    heading = soup.find(
        lambda tag: tag.name in {"h2", "h3"}
        and normalize_text(tag.get_text(" ", strip=True)) == "Abstract"
    )
    if not heading:
        return ""

    parts = []
    for sibling in heading.next_siblings:
        if getattr(sibling, "name", None) in {"h2", "h3"}:
            break

        if hasattr(sibling, "get_text"):
            text = sibling.get_text(" ", strip=True)
        else:
            text = str(sibling).strip()

        text = normalize_text(text)
        if text:
            parts.append(text)

    abstract = "\n\n".join(parts)
    if abstract.lower().startswith("no abstract is available"):
        return ""

    return abstract


def load_cached_abstracts():
    path = Path(OUTPUT_PATH)
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
            abstract = normalize_text(item.get("abstract", "")) if item.get("abstract") else ""
            if url and abstract:
                cached[url] = abstract

    return cached


def attach_abstracts(items, cached_abstracts, label, refresh=False):
    total = len(items)
    missing_count = 0

    for index, item in enumerate(items, start=1):
        url = item.get("url")
        if not url:
            continue

        abstract = ""
        if not refresh:
            abstract = cached_abstracts.get(url, "")

        if not abstract:
            abstract = extract_abstract(url)
            if abstract:
                cached_abstracts[url] = abstract
            else:
                missing_count += 1

        if abstract:
            item["abstract"] = abstract

        if index % 10 == 0 or index == total:
            print(f"{label}: {index}/{total}")

    if missing_count:
        print(f"{label}: {missing_count} items without abstract")


def extract_section_items(soup, anchor_name):
    anchor = soup.find("a", attrs={"name": anchor_name})
    if not anchor:
        return []

    items = []
    ol = anchor.find_next("ol")
    if not ol:
        return items

    for raw_item in ol.find_all("li", recursive=False):
        item_soup = BeautifulSoup(str(raw_item), "lxml").find("li")
        for extra_block in item_soup.select("div.publishedas, div.otherversion"):
            extra_block.decompose()

        links = item_soup.find_all("a", href=True)
        if len(links) < 2:
            continue

        title_link = links[0]
        venue_link = links[1]
        title = normalize_text(title_link.get_text(" ", strip=True))
        venue = normalize_text(venue_link.get_text(" ", strip=True))
        url = urllib.parse.urljoin(IDEAS_BASE_URL, title_link["href"])

        text = normalize_text(item_soup.get_text(" ", strip=True))
        match = re.match(r'^(?P<authors>.+),\s*(?P<year>\d{4})\.\s*"\s*(?P<title>.+?)\s*,"\s*(?P<rest>.*)$', text)
        if not match:
            continue

        authors = normalize_text(match.group("authors"))
        year = match.group("year")
        rest = normalize_text(match.group("rest"))

        tail = rest
        if tail.startswith(venue):
            tail = normalize_text(tail[len(venue):].lstrip(" ,"))

        items.append(
            {
                "title": title,
                "authors": authors,
                "venue": venue,
                "year": year,
                "url": url,
                "description": tail or "Paper record.",
                "linkLabel": "Open paper",
            }
        )

    return items


def build_data(refresh_abstracts=False):
    html = fetch_html(IDEAS_AUTHOR_URL)

    soup = BeautifulSoup(html, "lxml")
    cached_abstracts = load_cached_abstracts()
    cached_citations = load_cached_citations(OUTPUT_PATH)

    articles = extract_section_items(soup, "articles")
    working_papers = extract_section_items(soup, "papers")
    attach_abstracts(articles, cached_abstracts, "Articles", refresh=refresh_abstracts)
    attach_abstracts(working_papers, cached_abstracts, "Working papers", refresh=refresh_abstracts)
    attach_citations(articles, cached_citations, "Article citations")
    attach_citations(working_papers, cached_citations, "Working paper citations")

    for item in working_papers:
        item["status"] = item["year"]
        item["description"] = f"{item['authors']}. {item['venue']}. {item['description']}"
        item.pop("authors", None)
        item.pop("venue", None)
        item.pop("year", None)

    data = {
        "profileLinks": PROFILE_LINKS,
        "selectedPapers": articles,
        "workingPapers": working_papers,
        "ongoingProjects": ONGOING_PROJECTS,
        "policyPublications": POLICY_PUBLICATIONS,
        "resources": RESOURCES,
    }

    return data


def main():
    refresh_abstracts = "--refresh-abstracts" in sys.argv
    data = build_data(refresh_abstracts=refresh_abstracts)
    output_path = Path(OUTPUT_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    section_files = {
        "profileLinks": CONTENT_DIR / "profile-links.yml",
        "selectedPapers": CONTENT_DIR / "published-papers.yml",
        "workingPapers": CONTENT_DIR / "working-papers.yml",
        "ongoingProjects": CONTENT_DIR / "ongoing-projects.yml",
        "policyPublications": CONTENT_DIR / "policy-publications.yml",
        "resources": CONTENT_DIR / "resources.yml",
    }

    for key, path in section_files.items():
        with path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(
                data[key],
                handle,
                sort_keys=False,
                allow_unicode=True,
                width=1000,
            )

    subprocess.run([sys.executable, str(BUILD_SCRIPT)], check=True)

    print(
        textwrap.dedent(
            f"""
            Wrote {CONTENT_DIR / 'published-papers.yml'}
            Wrote {CONTENT_DIR / 'working-papers.yml'}
            Rebuilt {OUTPUT_PATH}
            Articles: {len(data['selectedPapers'])}
            Working papers: {len(data['workingPapers'])}
            Refresh abstracts: {'yes' if refresh_abstracts else 'no'}
            """
        ).strip()
    )


if __name__ == "__main__":
    main()
