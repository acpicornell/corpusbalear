# Corpus Balear — portal

[![Validate](https://github.com/acpicornell/corpusbalear/actions/workflows/validate.yml/badge.svg)](https://github.com/acpicornell/corpusbalear/actions/workflows/validate.yml)
[![Accessibility](https://github.com/acpicornell/corpusbalear/actions/workflows/a11y.yml/badge.svg)](https://github.com/acpicornell/corpusbalear/actions/workflows/a11y.yml)
[![Links](https://github.com/acpicornell/corpusbalear/actions/workflows/links.yml/badge.svg)](https://github.com/acpicornell/corpusbalear/actions/workflows/links.yml)

Landing hub for the **Corpus Balear**: a family of independent digital editions of
public-domain historical sources about the Balearic Islands — the great censuses and
gazetteers (1768–1881), early maps (Mut 1683, Despuig 1785) and present-day surname
(isonymy) studies.

The portal lives at the apex domain **<https://corpusbalear.org>** and links out to each project,
which is served from its own subdomain by its own Cloudflare Worker. It is a single static
page — vanilla HTML + CSS, no build step, no external requests; one small same-origin
script (`theme.js`) provides the light/dark toggle.

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
| Cronicón Mayoricense · 1881 | `cronicon.corpusbalear.org` |
| Isonímia mallorquina actual (INE 2025) | `llinatges.corpusbalear.org` |

The interface is in Catalan, as a deliberate cultural choice for the material.

## Content

- **Featured** — the aggregator, presented as the diachronic entry point.
- **Grouped cards** — *Censos i nomenclàtors*, *Mapes*, *Cròniques*
  (Cronicón Mayoricense), *Llinatges*.
- **Sobre el corpus** — what it is and the value of reading the sources in parallel.
- **Fonts, mètode i llicència** — the pipeline (facsimile → transcription → structured
  data → NGIB/Wikidata anchoring) and the licensing model.

### Licensing model (two layers)

- **Original sources** (old censuses, gazetteers, maps) are **public domain** by age.
- **What each project adds** (transcription, structured data, identifications, NGIB
  anchoring, georeferencing, code) is the author's own work, released openly: **code**
  under copyleft (e.g. AGPL-3.0), **curated data** under Creative Commons BY-NC. Each
  project states its exact terms. The `mapa-mut` project is the reference for this model.

## Run / deploy

```sh
python3 scripts/validate.py   # HTML, JSON-LD and link sanity checks
npx wrangler deploy           # web/ is served as static assets; no build step
```

## Documentation

- [docs/MAINTENANCE.md](docs/MAINTENANCE.md) — repository structure, continuous
  integration, deployment and custom domains, and how to add a project.
