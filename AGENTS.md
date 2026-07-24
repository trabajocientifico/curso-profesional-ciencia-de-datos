# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Overview

Static, single-page marketing/landing site (in Spanish) for the course
"Ciencia de Datos con Python + IA", plus an instructor profile page. There is
**no build system, no package manager, and no dependencies** — just hand-written
HTML files with all CSS and JavaScript inlined in `<style>`/`<script>` blocks.

- `index.html` — the course brochure. A full-screen, slide-based (horizontal
  carousel) presentation with a lead-capture modal form.
- `proximos_eventos/perfil.html` — instructor profile/CV page (Oscar Ivan
  Vargas Pineda), linked from `index.html`; links back via `Volver al curso`.
- `proximos_eventos/eventos.html` — upcoming-events agenda page (event cards
  with registration/Meet links), linked from the hero of `index.html`.
- `proximos_eventos/imagen/` — event poster images used by `eventos.html`.
- `proximos_eventos/perfil.png` — profile image asset, used by `perfil.html`
  in the same folder.

## Running / developing

There is no build or test step. Open the HTML files directly in a browser, or
serve the folder for accurate testing of `fetch`/navigation:

```bash
python -m http.server 8000    # then open http://localhost:8000/index.html
```

Deployment is a static file host (e.g. GitHub Pages); changes to the HTML are
the deliverable — no compile step.

## Architecture notes

**Everything lives in single files.** Each page bundles its own `<style>` and
`<script>`. When editing, keep CSS custom properties (the `:root { --neon, --bg,
... }` palette near the top of each file) as the single source of truth for
colors rather than hardcoding hex values in individual rules.

**`index.html` is responsive-hybrid**: on desktop (>820px) it behaves as a
full-screen slide carousel; on mobile (<=820px, the `@media (max-width:820px)`
block) the same `<section class="slide">` markup flows as a normal vertical
scroll page with a fixed bottom conversion bar (`#mobileBar`). The JS slide
engine (`go(i)` / `next()` / `prev()`, keyboard, swipe, wheel, auto-generated
dots) is desktop-only — every handler is guarded by `mobileMQ.matches`; on
mobile `go(i)` falls back to `scrollIntoView`. Adding a slide = add a
`<section class="slide">` in the markup; dots, progress bar, and counter derive
from `document.querySelectorAll('.slide')` automatically.

**Design system**: dark executive palette defined in `:root` — `--accent`
(cyan, reserved for CTAs and key data), `--gold` (dates/certificate),
`--danger` (form errors). Headings use Fraunces (`--font-display`), body uses
Inter (`--font-body`). Deliberately restrained: the only looping animation is
the `breath` pulse on the primary CTAs; avoid reintroducing glows, particles,
or extra accent colors.

**Lead form → Google Apps Script.** The modal form POSTs (as `FormData`, with
`mode: 'no-cors'`, so the response is opaque and cannot be read) to a Google
Apps Script web app. Configuration constants sit at the top of the `<script>`
in `index.html`:
- `APPS_SCRIPT_URL` — the deployed Apps Script endpoint that records submissions.
- `WA_NUMBER` / `WA_MSG_DEFAULT` — WhatsApp contact used to build `wa.me` links
  via `buildWaLink()`.

If the course date, WhatsApp number, or destination spreadsheet changes, update
these constants (and the `curso` value appended in the submit handler).

**Contact/social links** are hardcoded in `perfil.html` (YouTube @TCientifico,
trabajocientifico.org, LinkedIn, Google Scholar, GitHub, Instagram, phone,
email). Keep these consistent with any equivalent links in `index.html`.

## Content language

All user-facing copy is in Spanish. Match the existing tone and keep new copy in
Spanish.
