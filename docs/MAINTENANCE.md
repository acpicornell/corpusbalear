# Maintaining the portal

Repository layout, continuous integration, deployment, and how to add a project to the hub.

## Structure

- `web/` — static assets served by Cloudflare Workers Static Assets:
  - `index.html` — the hub page. Semantic HTML, `lang="ca"`, JSON-LD
    (`CollectionPage` + `Organization`), Open Graph, canonical.
  - `style.css` — shares the academic palette of the sibling sites (system serif,
    warm paper, brown accent, per-year colours). Full-bleed layout with
    viewport-relative margins. WCAG AA contrast; visible `:focus-visible` ring.
  - `theme.js` — light/dark theme toggle, shared with the sibling sites.
  - `robots.txt`, `sitemap.xml` — SEO.
  - `sitemap-index.xml` — sitemap index pointing at the portal's and every project's
    sitemap.
  - `_headers` — cache + security headers (CSP, `nosniff`, `Referrer-Policy`,
    `Permissions-Policy`).
- `scripts/validate.py` — HTML/JSON-LD/link sanity checks (see below).
- `scripts/check_site.py` — lints the site against the CSP its own `_headers` ships.
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
