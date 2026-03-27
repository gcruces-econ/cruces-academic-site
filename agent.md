# Project Context

- Project: Guillermo Cruces web presence.
- Current objective: maintain the academic website in a hand-editable Quarto workflow while preserving the existing custom design.
- Repository created on March 25, 2026 to track site, archive, and supporting materials cleanly.

# What Exists Today

- `site/` is a Quarto website project.
- `site/content/` is the main editorial layer and should be the default place for hand edits.
- `site/index.qmd` is now mostly the page shell and layout structure.
- `site/data/site-data.json` and `site/includes/generated/` are generated artifacts built from content files.
- `site/assets/documents/` contains the files currently linked from the public site.
- `archive/` contains the broader document library and legacy material that is not yet fully curated into the public page.
- `reference/gmail/` contains the original email/reference material that kicked off this work.
- `reference/screenshots/playwright/` contains screenshots of the prototype and visual references.

# Working Assumptions

- The Quarto site in `site/` is the canonical web source in this repository.
- Most future content edits should happen in `site/content/`, not in `index.qmd` or generated JSON.
- The current visual language should stay stable unless a future request explicitly asks for a redesign.
- The archive should stay organized but conservative: do not rename or move source documents casually once they are referenced from `site/content/` or linked public-facing files.

# Recommended Next Steps

1. Review `site/content/profile.yml` and the section YAML files against the latest CV and publication priorities.
2. Decide whether any sections should be broken into additional Quarto pages or remain on the current single-page layout.
3. Keep the GitHub Pages workflow healthy as Quarto and GitHub Actions evolve.
4. Continue using this repository for content curation, copy edits, link management, and light design iteration.

# Editing Conventions

- Prefer making visible content decisions in `site/content/`.
- Use `site/index.qmd` only for structure or section order.
- Keep research/source material in `archive/` unless the website needs to link to it directly.
- Put new references, screenshots, and briefing inputs in `reference/`.
- If the Quarto structure changes meaningfully, update this file so the next session starts with the right context.
