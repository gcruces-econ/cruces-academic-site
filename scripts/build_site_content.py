#!/usr/bin/env python3

import html
import json
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"
CONTENT_ROOT = SITE_ROOT / "content"
DATA_PATH = SITE_ROOT / "data" / "site-data.json"
GENERATED_INCLUDE_ROOT = SITE_ROOT / "includes" / "generated"


def load_yaml(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing content file: {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    return data if data is not None else []


def ensure_list(value, label):
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a YAML list")

    return value


def ensure_dict(value, label):
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a YAML mapping")

    return value


def render_profile_hero(profile):
    name = html.escape(profile["name"])
    bio = html.escape(profile["bio"])
    affiliations = profile.get("affiliations", [])
    portrait = ensure_dict(profile.get("portrait", {}), "profile.portrait")
    portrait_src = html.escape(portrait.get("src", "./assets/images/guillermo-cruces.jpg"))
    portrait_alt = html.escape(portrait.get("alt", "Portrait"))

    affiliation_markup = "\n".join(
        f"    <span>{html.escape(affiliation)}</span>" for affiliation in affiliations
    )

    return (
        "```{=html}\n"
        '<div class="hero-stage">\n'
        '  <figure class="portrait-frame">\n'
        f'    <img src="{portrait_src}" alt="{portrait_alt}" />\n'
        "  </figure>\n"
        '  <div class="hero-copy">\n'
        f"    <h1>{name}</h1>\n"
        '    <p class="hero-summary">\n'
        f"      {bio}\n"
        "    </p>\n"
        '    <div class="hero-meta" aria-label="Affiliations">\n'
        f"{affiliation_markup}\n"
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        "```\n"
    )


def render_footer(profile):
    email = html.escape(profile["email"])
    return f"```{{=html}}\n<p><a href=\"mailto:{email}\">{email}</a></p>\n```\n"


def build_site_data():
    profile = ensure_dict(load_yaml(CONTENT_ROOT / "profile.yml"), "profile.yml")
    profile_links = ensure_list(load_yaml(CONTENT_ROOT / "profile-links.yml"), "profile-links.yml")
    published_papers = ensure_list(
        load_yaml(CONTENT_ROOT / "published-papers.yml"), "published-papers.yml"
    )
    working_papers = ensure_list(
        load_yaml(CONTENT_ROOT / "working-papers.yml"), "working-papers.yml"
    )
    ongoing_projects = ensure_list(
        load_yaml(CONTENT_ROOT / "ongoing-projects.yml"), "ongoing-projects.yml"
    )
    policy_publications = ensure_list(
        load_yaml(CONTENT_ROOT / "policy-publications.yml"), "policy-publications.yml"
    )
    resources = ensure_list(load_yaml(CONTENT_ROOT / "resources.yml"), "resources.yml")

    portrait = ensure_dict(profile.get("portrait", {}), "profile.portrait")

    site_data = {
        "profile": {
            "name": profile["name"],
            "bio": profile["bio"],
            "affiliations": profile.get("affiliations", []),
            "email": profile["email"],
            "portrait": {
                "src": portrait.get("src", "./assets/images/guillermo-cruces.jpg"),
                "alt": portrait.get("alt", "Portrait"),
            },
        },
        "profileLinks": profile_links,
        "selectedPapers": published_papers,
        "workingPapers": working_papers,
        "ongoingProjects": ongoing_projects,
        "policyPublications": policy_publications,
        "resources": resources,
    }

    return profile, site_data


def write_outputs(profile, site_data):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_INCLUDE_ROOT.mkdir(parents=True, exist_ok=True)

    DATA_PATH.write_text(
        json.dumps(site_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (GENERATED_INCLUDE_ROOT / "profile-hero.qmd").write_text(
        render_profile_hero(profile),
        encoding="utf-8",
    )
    (GENERATED_INCLUDE_ROOT / "footer-email.qmd").write_text(
        render_footer(profile),
        encoding="utf-8",
    )


def main():
    profile, site_data = build_site_data()
    write_outputs(profile, site_data)

    print(f"Wrote {DATA_PATH.relative_to(REPO_ROOT)}")
    print(
        "Built content from "
        + ", ".join(
            [
                "profile.yml",
                "profile-links.yml",
                "published-papers.yml",
                "working-papers.yml",
                "ongoing-projects.yml",
                "policy-publications.yml",
                "resources.yml",
            ]
        )
    )


if __name__ == "__main__":
    main()
