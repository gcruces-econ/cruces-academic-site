# Project Context

- Project: Guillermo Cruces web presence.
- Current objective: organize the research archive and use the existing static prototype to build a Google Site for Guillermo Cruces.
- Repository created on March 25, 2026 to start tracking changes cleanly.

# What Exists Today

- `site/` contains a polished static prototype with curated sections for profile, selected research, working papers, policy publications, and resources.
- `site/data.js` is the main content source for the current prototype.
- `site/assets/documents/` contains the documents currently linked from the prototype.
- `archive/` contains the broader document library and legacy materials that are not yet fully curated into the site.
- `reference/gmail/` contains the original email/reference material that kicked off this work.
- `reference/screenshots/playwright/` contains screenshots of the prototype captured on March 16, 2026.

# Working Assumptions

- The static prototype is not necessarily the final published site.
- The final destination we are steering toward is a Google Site, so structure, copy, and asset selection matter more than framework work.
- The archive should stay organized but conservative: do not rename or move source documents casually once they are referenced from `site/data.js`.

# Recommended Next Steps

1. Translate the current prototype sections into a concrete Google Site page map.
2. Review `site/data.js` against the latest CV and decide what stays, what is added, and what is removed.
3. Decide which files should be embedded, linked from Drive, or kept only as back-office archive material.
4. Use this repository for content curation, copy edits, structure decisions, and link management while the Google Site is assembled.

# Editing Conventions

- Prefer making visible content decisions in `site/data.js` and `site/index.html`.
- Keep research/source material in `archive/` unless the prototype needs to link to it directly.
- Put new references, screenshots, and briefing inputs in `reference/`.
- If the Google Site structure changes meaningfully, update this file so the next session has the right context.
