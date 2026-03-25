#!/usr/bin/env python3

import json
import re
import textwrap
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

IDEAS_AUTHOR_URL = "https://ideas.repec.org/e/pcr20.html"
IDEAS_BASE_URL = "https://ideas.repec.org"
OUTPUT_PATH = "site/data.js"

PROFILE_LINKS = [
    {
        "title": "Current CV",
        "description": "PDF linked from Guillermo Cruces's current site.",
        "url": "https://www.dropbox.com/s/u88tuj8n3hh9asl/CV_CRUCES_2023_EN_Web.pdf?dl=0",
        "linkLabel": "Open PDF",
    },
    {
        "title": "Google Scholar",
        "description": "Citation profile and indexed publications.",
        "url": "https://scholar.google.com/citations?user=CylXqSUAAAAJ&hl=en",
        "linkLabel": "Open profile",
    },
    {
        "title": "IDEAS/RePEc",
        "description": "Author page used as the source for published and working paper links.",
        "url": "https://ideas.repec.org/e/pcr20.html",
        "linkLabel": "Open author page",
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
        "description": "Department page linked from Guillermo Cruces's current site.",
        "url": "https://www.nottingham.ac.uk/economics/",
        "linkLabel": "Open site",
    },
    {
        "title": "IZA",
        "description": "IZA profile linked from the current site.",
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
            return repaired

    return value


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
                "description": tail or "IDEAS/RePEc record.",
                "linkLabel": "View on IDEAS",
            }
        )

    return items


def build_data():
    with urllib.request.urlopen(IDEAS_AUTHOR_URL) as response:
        html = response.read().decode("utf-8", errors="ignore")

    soup = BeautifulSoup(html, "lxml")

    articles = extract_section_items(soup, "articles")
    working_papers = extract_section_items(soup, "papers")

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
    data = build_data()

    output = "// Generated from IDEAS/RePEc author page pcr20.\n"
    output += "window.siteData = "
    output += json.dumps(data, ensure_ascii=False, indent=2)
    output += ";\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(output)

    print(
        textwrap.dedent(
            f"""
            Wrote {OUTPUT_PATH}
            Articles: {len(data['selectedPapers'])}
            Working papers: {len(data['workingPapers'])}
            """
        ).strip()
    )


if __name__ == "__main__":
    main()
