# Guillermo Cruces Web Project

This repository tracks the working materials for Guillermo Cruces's academic website.

The current workflow is:

1. maintain a clean static reference site in `site/`
2. keep supporting documents and older source material organized in `archive/`
3. preserve screenshots and external references in `reference/`
4. document project context for future sessions in `agent.md`

## What The Repository Is For

- `site/` is the working website we edit.
- `scripts/` contains utilities that generate or refresh data used by the website.
- `archive/` stores broader source material that is useful for migration, reference, or future curation, but is not necessarily shown on the live page.
- `reference/` stores outside references and screenshots that help guide layout/content decisions.
- root-level docs explain the repo and preserve working context between sessions.

## Top-Level Files

- `README.md`
  Explains the structure of the repository, what each important folder/file does, and how to preview or update the site.

- `agent.md`
  Session memory for future Codex work. It describes the current objective, the current site state, and conventions we want to preserve in later sessions.

- `.gitignore`
  Prevents local-only files from being committed. This currently ignores macOS metadata, temporary folders, Playwright/test artifacts, editor settings, and Python cache folders.

## Main Folders

### `site/`

This is the active website.

Files in `site/`:

- `site/index.html`
  Main HTML document for the site. It defines the page structure: navigation, hero section, published papers, working papers, ongoing projects, policy publications, and footer.

- `site/styles.css`
  Main stylesheet for the site. It controls typography, color palette, spacing, layout, hero composition, cards, abstracts, responsive behavior, and visual identity.

- `site/script.js`
  Frontend behavior for the site. It renders profile links, papers, working papers, ongoing projects, and policy publications from `site/data.js`. It also powers search and abstract expand/collapse buttons.

- `site/data.js`
  Content payload consumed by `site/script.js`. It contains the structured data for profile links, published papers, working papers, ongoing projects, policy publications, and any other rendered content blocks. This file is generated/refreshed by `scripts/sync_ideas_data.py`.

- `site/favicon.svg`
  Favicon used by the website tab.

#### `site/assets/`

Static assets used by the site.

#### `site/assets/images/`

- `site/assets/images/guillermo-cruces.jpg`
  Portrait used in the hero section.

#### `site/assets/documents/`

This folder contains files that the website may link to directly.

Important items currently used or kept ready for use:

- `site/assets/documents/CV_CRUCES_2026_EN.doc`
  Local CV working document kept in the repo.

- `site/assets/documents/publicaciones.pdf`
  Legacy compiled publications PDF.

- `site/assets/documents/CONICET publicaciones.pdf`
  Additional compiled publication list.

- `site/assets/documents/publicaciones.zip`
  Historic bundle of publication-related materials.

- `site/assets/documents/CRUCES LEVY 2022 undp-rblac-PNUD_bckPapers24-OK.pdf`
- `site/assets/documents/Book Cruces Fields Jaume Viollaz 2017 OUP WIDER.pdf`
- `site/assets/documents/Cruces Garcia-Domench Gasparini Falling Inequality Chapter 15 OUP 2013.pdf`
- `site/assets/documents/Bergolo Cruces IZA proof chapter4.pdf`
- `site/assets/documents/Gasparini Cruces Distribution in motion Argentina doc_cedlas 78 2008.pdf`
- `site/assets/documents/Los programas sociales en Argentina BAJA.pdf`
  These are currently used by the policy/books section of the site.

The rest of the PDFs in this folder are direct-access copies of publications or related documents that may be useful for curation, backup, or future sections.

### `scripts/`

Utilities used to maintain the site data.

- `scripts/sync_ideas_data.py`
  Main sync script for publication data. It fetches Guillermo Cruces's publication listings, rebuilds `site/data.js`, keeps link metadata updated, and stores abstracts when available. This is the file to run whenever we want to refresh the publication lists.

### `archive/`

Long-term storage for source material that is useful to keep in the repository but is not part of the page structure itself.

#### `archive/library/`

Large document library containing publications, drafts, appendices, reports, thesis material, policy papers, and other source files related to Guillermo Cruces's work.

This is the broadest research archive in the repo. Use it when:

- looking for a publication not currently exposed in `site/`
- checking alternate versions of papers
- recovering background documents for future site sections
- comparing old and new versions of the same work

#### `archive/collections/`

Grouped source packages kept together because they belong to a specific theme or source bundle.

Current subfolders:

- `archive/collections/dp/`
  Collection folder reserved for grouped discussion-paper material.

- `archive/collections/wb-poverty-assessment/`
  Collection folder reserved for World Bank poverty-assessment related material.

#### `archive/legacy/`

Superseded or older material preserved mainly for context.

Current subfolders:

- `archive/legacy/old/`
  Older files that were kept rather than deleted, usually because they may still be useful historically or editorially.

### `reference/`

Reference material that informs design/content decisions but is not part of the website itself.

#### `reference/gmail/`

Materials captured from Gmail or email threads.

- `reference/gmail/Gmail - pagina web.pdf`
  PDF export of an email reference related to the website.

- `reference/gmail/gmail_ref-1.png`
- `reference/gmail/gmail_ref-2.png`
  Screenshot references from Gmail.

#### `reference/screenshots/`

Folder for screenshots of the website and related UI states.

- `reference/screenshots/playwright/`
  Intended location for browser-generated screenshots captured during local verification or design review.

### `output/`

Local-only output folder for generated artifacts and checks. This is ignored by git.

#### `output/playwright/`

Used for temporary browser screenshots captured while visually checking layout changes.

## How The Site Works

The website is a static site with no framework.

Flow:

1. `site/index.html` defines the sections and placeholders.
2. `site/data.js` provides structured content.
3. `site/script.js` reads `window.siteData` and renders the dynamic lists.
4. `site/styles.css` defines the visual system and responsive layout.

## How To Preview The Site

From the repository root, run:

```bash
python3 -m http.server
```

Then open:

[http://localhost:8000/site/](http://localhost:8000/site/)

## How To Refresh Publication Data

Run:

```bash
python3 scripts/sync_ideas_data.py
```

What this does:

- refreshes publication and working paper entries
- refreshes profile link metadata stored in `site/data.js`
- attempts to fetch and cache abstracts
- rewrites `site/data.js`

If we ever need to force a fresh abstract pass instead of reusing cached abstracts from the existing `site/data.js`, run:

```bash
python3 scripts/sync_ideas_data.py --refresh-abstracts
```

## Editing Guidance

- Edit `site/index.html` when changing structure or section order.
- Edit `site/styles.css` when changing visual design or responsive behavior.
- Edit `site/script.js` when changing rendering behavior, search behavior, or abstract interactions.
- Run `scripts/sync_ideas_data.py` when publication lists or abstracts need refreshing.
- Use `site/assets/documents/` only for files the website may need to link directly.
- Use `archive/` for broader storage, not for files that must be directly referenced by the site UI.

## Current Project Intent

This repo is being used to shape and maintain Guillermo Cruces's web presence with a structure that is easy to edit, version, and reuse in future iterations.
