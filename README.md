# Corpus Balear — portal

Landing hub for the **Corpus Balear**: a family of independent digital editions of
public-domain historical sources about the Balearic Islands (censuses and gazetteers
1768–1881, early maps, and surname studies).

The portal lives at the apex domain **`corpusbalear.org`** and links out to each project,
which is served from its own subdomain (`<slug>.corpusbalear.org`) by its own Worker.

## Structure

- `web/` — static assets served by Cloudflare Workers Static Assets:
  - `index.html` — the hub page (grouped cards + featured aggregator), Catalan.
  - `style.css` — shares the academic palette of the sibling sites.
  - `robots.txt`, `sitemap.xml` — SEO.
  - `_headers` — cache + security headers.
- `wrangler.jsonc` — Worker config (`name: corpusbalear-portal`, assets from `web/`).

## Deploy

```sh
npx wrangler deploy
```

Then attach the custom domains `corpusbalear.org` and `www.corpusbalear.org` to this Worker
in the Cloudflare dashboard (Workers → this worker → Custom Domains). SSL is provisioned
automatically.

## Adding a project

Add a `<a class="card" href="https://<slug>.corpusbalear.org/">` entry to the right section
in `index.html`, and a matching `hasPart` entry in the JSON-LD block.
