# Guillermo Cruces Web Project

This repository maintains Guillermo Cruces's academic website and its supporting source material.

The website now lives in `site/` as a Quarto project, so the content is easier to edit by hand while keeping the existing custom visual design.

## Repository Structure

- `site/`
  The active Quarto website project.

- `scripts/`
  Utilities that refresh structured site data.

- `archive/`
  Long-term storage for papers, reports, drafts, and legacy source material that is useful for curation but is not necessarily linked on the public page.

- `reference/`
  Screenshots, email exports, and other reference material that helps guide layout and editorial decisions.

- `.github/workflows/publish.yml`
  GitHub Pages workflow that renders the Quarto project in `site/` and deploys it automatically from `main`.

## Website Files

Important files in `site/`:

- `site/_quarto.yml`
  Quarto project configuration. It enables website output, registers static resources, loads the shared stylesheet, and includes the custom head partial.

- `site/index.qmd`
  Main page source. This is the best place to edit page structure, headings, hero copy, and section order.

- `site/styles.css`
  Custom stylesheet preserving the current visual identity.

- `site/script.js`
  Frontend behavior for search, abstract toggles, and dynamic rendering of lists from JSON data.

- `site/data/site-data.json`
  Structured content payload for profile links, papers, working papers, ongoing projects, and policy publications. This is the main hand-editable data file.

- `site/includes/head.html`
  Shared head include for the favicon and font loading.

- `site/assets/`
  Static assets used by the website.

## Publishing Flow

The recommended flow is:

1. edit `site/index.qmd` for layout and copy
2. edit `site/data/site-data.json` for papers, links, and structured records
3. edit `site/styles.css` when the visual system needs changes
4. preview locally with Quarto
5. push to `main` to let GitHub Actions render and publish the site

## Local Preview

From the repository root:

```bash
cd site
quarto preview
```

Quarto is not bundled in this repository, so it must be installed locally for preview and render commands to work.

## Refreshing Publication Data

Run:

```bash
python3 scripts/sync_ideas_data.py
```

This script:

- fetches publication and working paper entries from IDEAS/RePEc
- refreshes cached abstracts where available
- rewrites `site/data/site-data.json`

To force a fresh abstract pass:

```bash
python3 scripts/sync_ideas_data.py --refresh-abstracts
```

## Editing Guidance

- Prefer `site/index.qmd` for visible page structure and copy changes.
- Prefer `site/data/site-data.json` for repeatable content lists and link metadata.
- Keep `site/assets/documents/` for files that the public site should link directly.
- Keep broader backups and research material in `archive/`.
- Keep screenshots and external references in `reference/`.

## GitHub Pages Notes

The repo includes a Quarto GitHub Pages workflow in `.github/workflows/publish.yml`.

- It renders the Quarto project in `site/`.
- It uploads `site/_site` as the Pages artifact.
- It deploys automatically on pushes to `main` and on manual workflow runs.

## Current Intent

The current goal is to maintain a visually polished academic website with a lightweight authoring workflow: Quarto for structure, JSON for hand-editable data, custom CSS for the existing look, and GitHub Pages for deployment.
