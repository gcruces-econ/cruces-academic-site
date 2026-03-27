# Guillermo Cruces Web Project

This repository maintains Guillermo Cruces's academic website and its supporting source material.

The site is built with Quarto, but the editing workflow is intentionally simpler than “edit the page HTML”:

- profile details live in a small YAML file
- links and section content live in separate YAML files
- a build script regenerates the runtime JSON automatically
- GitHub Actions renders and deploys the site on every push to `main`

## Repository Structure

- `site/`
  The active Quarto website project.

- `site/content/`
  The main hand-editable content files. This is where most edits should happen.

- `scripts/`
  Utilities that rebuild site data or refresh publication data from IDEAS/RePEc.

- `archive/`
  Long-term storage for papers, reports, drafts, and legacy source material that is useful for curation but is not necessarily linked on the public page.

- `reference/`
  Screenshots, email exports, and other reference material that helps guide layout and editorial decisions.

- `.github/workflows/publish.yml`
  GitHub Pages workflow that renders the Quarto project in `site/` and deploys it automatically from `main`.

## What To Edit

For almost all manual edits, use files in `site/content/`:

- `site/content/profile.yml`
  Name, bio, affiliations, portrait, and footer email.

- `site/content/profile-links.yml`
  Hero links such as CV, email, Google Scholar, and external profiles.

- `site/content/published-papers.yml`
  Published papers.

- `site/content/working-papers.yml`
  Working paper archive.

- `site/content/ongoing-projects.yml`
  Current projects.

- `site/content/policy-publications.yml`
  Policy, report, and book items.

- `site/content/README.md`
  Short in-folder editing guide with examples.

Files that are generated and normally should not be edited by hand:

- `site/data/site-data.json`
  Generated runtime data consumed by the frontend.

- `site/includes/generated/profile-hero.qmd`
- `site/includes/generated/footer-email.qmd`
  Generated includes built from `site/content/profile.yml`.

## Website Files

- `site/_quarto.yml`
  Quarto project configuration. It registers assets, adds the pre-render build step, and loads the shared stylesheet and head include.

- `site/index.qmd`
  Main page shell. It is now mostly layout, not content entry.

- `site/styles.css`
  Custom stylesheet preserving the current visual identity.

- `site/script.js`
  Frontend behavior for search and abstract toggles using generated site data.

- `scripts/build_site_content.py`
  Rebuilds generated site files from the content YAML files.

- `scripts/sync_ideas_data.py`
  Refreshes published and working paper data from IDEAS/RePEc, writes the hand-editable YAML section files, then rebuilds generated site files.

## Simplest Editing Flow

### Change the bio

Edit:

- `site/content/profile.yml`

### Add a published paper

Edit:

- `site/content/published-papers.yml`

Add another list item using the same shape as the entries already in the file.

### Add a working paper

Edit:

- `site/content/working-papers.yml`

### Change hero links

Edit:

- `site/content/profile-links.yml`

## Edit Directly On GitHub

For quick edits in the browser:

1. open the repository on GitHub
2. edit a file under `site/content/`
3. commit the change to `main`
4. GitHub Actions will rebuild and publish the site automatically

That means most routine edits do not require touching `index.qmd`, `script.js`, or `site-data.json`.

## Local Preview

From the repository root:

```bash
cd site
quarto preview
```

The Quarto project runs a pre-render step automatically:

```bash
python3 ../scripts/build_site_content.py
```

If you want to rebuild generated files manually without previewing:

```bash
python3 scripts/build_site_content.py
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
- rewrites `site/content/published-papers.yml`
- rewrites `site/content/working-papers.yml`
- rebuilds generated site files

To force a fresh abstract pass:

```bash
python3 scripts/sync_ideas_data.py --refresh-abstracts
```

## Editing Guidance

- Prefer `site/content/` for content changes.
- Use `site/index.qmd` only for layout or section-order changes.
- Use `site/styles.css` for visual changes.
- Keep `site/assets/documents/` for files that the public site should link directly.
- Keep broader backups and research material in `archive/`.
- Keep screenshots and external references in `reference/`.

## GitHub Pages Notes

The repo includes a Quarto GitHub Pages workflow in `.github/workflows/publish.yml`.

- It renders the Quarto project in `site/`.
- It uploads `site/_site` as the Pages artifact.
- It deploys automatically on pushes to `main` and on manual workflow runs.

## Current Intent

The current goal is to maintain a visually polished academic website with a lightweight authoring workflow: small editable content files in `site/content/`, generated site data, custom CSS for the existing look, and GitHub Pages for deployment.
