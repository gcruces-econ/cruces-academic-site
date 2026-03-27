# Editing Guide

These are the files you should edit by hand.

- `profile.yml`
  Name, bio, affiliations, portrait, and footer email.

- `profile-links.yml`
  Hero links such as CV, email, Google Scholar, or profile pages.

- `published-papers.yml`
  Published papers shown in the main research section.

- `working-papers.yml`
  Working papers shown in the archive section.

- `ongoing-projects.yml`
  Current projects shown in the right-hand work column.

- `policy-publications.yml`
  Policy, report, and book items shown in the policy section.

- `resources.yml`
  Extra resource links kept for future use.

## Quick Examples

Change the bio:

```yaml
name: Guillermo A. Cruces
bio: Professor of Economics at ...
```

Add a published paper:

```yaml
- title: Example paper title
  authors: Author One & Author Two
  venue: Journal Name
  year: "2026"
  url: https://example.com/paper
  description: Publisher, volume, or short note.
  linkLabel: Open paper
  abstract: Optional abstract text.
```

After editing these files, Quarto regenerates the site data automatically during render. To rebuild locally without previewing, run:

```bash
python3 scripts/build_site_content.py
```
