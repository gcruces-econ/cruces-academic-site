# Guillermo Cruces Web Project

This repository tracks the working materials for Guillermo Cruces's web presence.

The current goal is to use the existing static prototype as a reference while we organize content and migrate the structure into a Google Site.

## Repository Layout

- `site/`: current static prototype in HTML, CSS, and vanilla JavaScript.
- `site/assets/documents/`: documents linked directly from the prototype.
- `archive/library/`: broader source library that is not yet surfaced in the prototype.
- `archive/collections/`: grouped document collections kept for reference.
- `archive/legacy/`: older or superseded materials preserved for context.
- `reference/`: briefing material and visual references, including screenshots of the prototype.
- `agent.md`: session context and working notes for future Codex runs.

## Previewing The Prototype

From the repository root, run:

```bash
python3 -m http.server
```

Then open [http://localhost:8000/site/](http://localhost:8000/site/).

## Working Notes

- `site/data.js` is the curated content inventory for the current prototype.
- If a linked document is moved or renamed, update the corresponding entry in `site/data.js`.
- Keep `archive/` as the long-term source library and use `site/assets/documents/` only for files that the prototype currently exposes.
- The static site is a reference implementation; the publication target we are working toward is a Google Site.
