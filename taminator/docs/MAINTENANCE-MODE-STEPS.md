# Put taminator.dev (GitHub Pages) into maintenance mode

## Option A: Replace site with a single maintenance page (recommended)

1. **Find the repo and branch that GitHub Pages uses for taminator.dev**
   - GitHub repo: Settings → Pages → "Build and deployment" → Source (e.g. "Deploy from a branch" and which branch/folder).
   - Custom domain taminator.dev is set under Settings → Pages → Custom domain.

2. **In that repo, replace the published content with only the maintenance page:**
   - If the source is **"Branch: gh-pages" / root**:  
     In that repo, on the `gh-pages` branch, delete all files except one: `index.html`. Put the contents of `taminator/docs/maintenance-mode-index.html` (from this repo) into that root `index.html`. Commit and push.
   - If the source is **"Branch: main, folder: /docs"**:  
     In that repo, under `docs/`, remove everything except one file. Rename or replace `docs/index.html` with the maintenance page content. (Or make `docs/` contain only `index.html` with the maintenance content.) Commit and push.

3. **Result:** Every request to taminator.dev (and any path) may still hit existing paths if the server returns cached or old content. To force a single maintenance experience:
   - Either ensure the theme/build outputs only one page (e.g. MkDocs "single page" or a static site that redirects everything to `/` or `/index.html`), or
   - Add a `404.html` in the same root that contains the same maintenance HTML so unknown paths also show maintenance.

4. **Re-enable later:** When the customer data is redacted, restore the real docs (from a branch or backup), fix content, then switch the Pages source back or push the fixed site.

## Option B: Disable GitHub Pages

1. In the GitHub repo that has taminator.dev as custom domain: **Settings → Pages**.
2. Under "Build and deployment", set **Source** to **None** (or disable Pages).
3. Save. The site will go down; visitors will see a GitHub 404 or "There isn't a GitHub Pages site here."
4. When ready, re-enable Pages and point it at a branch/folder that contains only redacted content (or the maintenance page).

## Maintenance page file

Use the contents of **`taminator/docs/maintenance-mode-index.html`** in this repo as your single `index.html` (and optionally `404.html`) when replacing the site.

The maintenance page includes `<meta name="robots" content="noindex, nofollow">` to discourage indexing of the maintenance state.

## After maintenance

- Redact all customer data (names, emails, phones, account numbers) from the docs source before republishing.
- Request removal of cached copies from search engines (e.g. Google Search Console removal for the affected URLs).
