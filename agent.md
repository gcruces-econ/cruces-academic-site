# Project Context

- Project: Guillermo Cruces web presence.
- Current objective: maintain the academic website in a hand-editable Quarto workflow while preserving the existing custom design.
- Repository created on March 25, 2026 to track site, archive, and supporting materials cleanly.

# What Exists Today

- `site/` is now a Quarto website project.
- `site/index.qmd` is the main page source for layout and copy.
- `site/data/site-data.json` is the primary structured content source.
- `site/assets/documents/` contains the files currently linked from the public site.
- `archive/` contains the broader document library and legacy material that is not yet fully curated into the public page.
- `reference/gmail/` contains the original email/reference material that kicked off this work.
- `reference/screenshots/playwright/` contains screenshots of the prototype and visual references.

# Working Assumptions

- The Quarto site in `site/` is now the canonical web source in this repository.
- The current visual language should stay stable unless a future request explicitly asks for a redesign.
- The archive should stay organized but conservative: do not rename or move source documents casually once they are referenced from `site/data/site-data.json`.

# Recommended Next Steps

1. Review `site/data/site-data.json` against the latest CV and publication priorities.
2. Decide whether any sections should be broken into additional Quarto pages or remain on the current single-page layout.
3. Confirm the target GitHub Pages repository settings once deployment is connected.
4. Continue using this repository for content curation, copy edits, link management, and light design iteration.

# Editing Conventions

- Prefer making visible content decisions in `site/index.qmd` and `site/data/site-data.json`.
- Keep research/source material in `archive/` unless the website needs to link to it directly.
- Put new references, screenshots, and briefing inputs in `reference/`.
- If the Quarto structure changes meaningfully, update this file so the next session starts with the right context.
