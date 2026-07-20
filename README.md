# Corpus Balear — portal

[![Validate](https://github.com/acpicornell/corpusbalear/actions/workflows/validate.yml/badge.svg)](https://github.com/acpicornell/corpusbalear/actions/workflows/validate.yml)
[![Accessibility](https://github.com/acpicornell/corpusbalear/actions/workflows/a11y.yml/badge.svg)](https://github.com/acpicornell/corpusbalear/actions/workflows/a11y.yml)
[![Links](https://github.com/acpicornell/corpusbalear/actions/workflows/links.yml/badge.svg)](https://github.com/acpicornell/corpusbalear/actions/workflows/links.yml)

Landing hub for the **Corpus Balear**: a family of independent digital editions of
public-domain historical sources about the Balearic Islands — the great censuses and
gazetteers (1768–1881), early maps (Mut 1683, Despuig 1785) and present-day surname
(isonymy) studies.

The portal lives at the apex domain **`corpusbalear.org`** and links out to each project,
which is served from its own subdomain by its own Cloudflare Worker. It is a single static
page — vanilla HTML + CSS, no build step, no JavaScript, no external requests.

## Projects linked

| Project | Subdomain |
|---|---|
| Nomenclàtors balears (diachronic aggregator) | `nomenclators.corpusbalear.org` |
| Cens d'Aranda · 1768 | `aranda.corpusbalear.org` |
| Cens de Floridablanca · 1787 | `floridablanca.corpusbalear.org` |
| Diccionari de Miñano · 1826 | `minano.corpusbalear.org` |
| Diccionari de Madoz · 1845 | `madoz.corpusbalear.org` |
| Nomenclàtor · 1860 | `1860.corpusbalear.org` |
| Diccionari de Riera · 1881 | `riera.corpusbalear.org` |
| Mapa de Vicenç Mut · 1683 | `mut.corpusbalear.org` |
| Mapa del cardenal Despuig · 1785 | `despuig.corpusbalear.org` |
| Isonímia mallorquina actual (INE 2025) | `llinatges.corpusbalear.org` |

The interface is in Catalan, as a deliberate cultural choice for the material.

## Content

- **Featured** — the aggregator, presented as the diachronic entry point.
- **Grouped cards** — *Censos i nomenclàtors*, *Mapes*, *Llinatges*.
- **Sobre el corpus** — what it is and the value of reading the sources in parallel.
- **Fonts, mètode i llicència** — the pipeline (facsimile → transcription → structured
  data → NGIB/Wikidata anchoring) and the licensing model.

### Licensing model (two layers)

- **Original sources** (old censuses, gazetteers, maps) are **public domain** by age.
- **What each project adds** (transcription, structured data, identifications, NGIB
  anchoring, georeferencing, code) is the author's own work, released openly: **code**
  under copyleft (e.g. AGPL-3.0), **curated data** under Creative Commons BY-NC. Each
  project states its exact terms. The `mapa-mut` project is the reference for this model.

## Structure

- `web/` — static assets served by Cloudflare Workers Static Assets:
  - `index.html` — the hub page. Semantic HTML, `lang="ca"`, JSON-LD
    (`CollectionPage` + `Organization`), Open Graph, canonical.
  - `style.css` — shares the academic palette of the sibling sites (system serif,
    warm paper, brown accent, per-year colours). Full-bleed layout with
    viewport-relative margins. WCAG AA contrast; visible `:focus-visible` ring.
  - `robots.txt`, `sitemap.xml` — SEO.
  - `_headers` — cache + security headers (CSP, `nosniff`, `Referrer-Policy`,
    `Permissions-Policy`).
- `wrangler.jsonc` — Worker config (`name: corpusbalear-portal`, assets from `web/`).

## Continuous integration

GitHub Actions run on every push and pull request (`.github/workflows/`):

- **validate** — `scripts/validate.py` (standard library only): HTML sanity, JSON-LD
  validity, internal-anchor resolution, relative-asset existence, and that the project
  cards and the JSON-LD `hasPart` graph list the same URLs. Run locally with
  `python3 scripts/validate.py`.
- **a11y** — serves the site and runs [pa11y](https://pa11y.org/) at WCAG 2.1 AA.
- **links** — [lychee](https://lychee.cli.rs/) checks external links stay alive (the
  `corpusbalear.org` hosts are excluded until deployed).
- **deploy** — `wrangler deploy` on push to main. Inert until a `CLOUDFLARE_API_TOKEN`
  repository secret is set (the guard step skips it so the run stays green meanwhile).

## Deploy

```sh
npx wrangler deploy
```

Then attach the custom domains `corpusbalear.org` and `www.corpusbalear.org` to this Worker
(Cloudflare dashboard → Workers → this worker → Custom Domains). TLS is provisioned and
renewed automatically; enable **Always Use HTTPS** on the zone.

## Adding a project

Add an `<a class="card" href="https://<slug>.corpusbalear.org/">` entry to the right
section in `index.html`, plus a matching `hasPart` entry in the JSON-LD block. When the
Menorca and Eivissa isonymy studies are ready, they join the *Llinatges* section.
