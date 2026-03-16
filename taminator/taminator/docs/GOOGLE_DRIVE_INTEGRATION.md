# Google Drive and Docs Integration

Taminator can create Google Docs from report content and (optionally) list or store reports in a Google Drive folder. This doc describes the design and setup.

## Scope

- **Create Doc from report:** Turn a local report (by customer name) into a new Google Doc and open it in the browser. Uses Drive API to create a file with `application/vnd.google-apps.document` and upload the markdown/text content.
- **Library in UI:** The browser UI has a **Library** tab that lists all reports found in local search paths (grouped by account). Each report can be **View**ed or **Open in Google Docs** (creates the Doc and opens the URL in a new tab).
- **OAuth2:** User authorizes Taminator once; refresh token is stored in `~/.config/taminator/google_token.json` so the app can create docs without prompting every time.

## Quick setup

1. Create OAuth2 credentials in Google Cloud Console (see Prerequisites below).
2. Set environment variables or add `~/.config/taminator/google_credentials.json`:
   - `TAMINATOR_GOOGLE_CLIENT_ID`
   - `TAMINATOR_GOOGLE_CLIENT_SECRET`
3. Run once: `tam-rfe google-connect` — a browser opens; sign in and allow access. The refresh token is saved.
4. In the web UI, open the **Library** tab and use **Open in Google Docs** on any report.

## Prerequisites

1. **Google Cloud project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a project (or use an existing one).
   - Enable **Google Drive API** (and optionally **Google Docs API** if we use it for richer content).

2. **OAuth 2.0 credentials**
   - APIs & Services → Credentials → Create Credentials → OAuth client ID.
   - Application type: **Desktop app** (for local `tam-rfe serve`) or **Web application** if you later host the UI.
   - Note the **Client ID** and **Client secret**; they are used in Taminator config.

3. **OAuth consent screen**
   - Configure consent screen (e.g. External), add scopes:
     - `https://www.googleapis.com/auth/drive.file` — Create and manage files created by the app.
     - Optionally `https://www.googleapis.com/auth/drive` or `docs` if you need broader access.

## How it works

- **Token storage:** Taminator stores the Google refresh token in the same way as other tokens (e.g. `~/.config/taminator/` or keyring). Client ID and secret can live in config or environment variables.
- **Create Doc:** When the user clicks "Open in Google Docs" for a report:
  1. Backend reads the report file (by customer name) or receives content from the UI.
  2. Backend uses the Drive API to create a new file with MIME type `application/vnd.google-apps.document` and the report text as the initial content (Drive converts uploads to Doc format).
  3. Backend returns the document’s `webViewLink`; the UI opens it in a new tab.
- **Library:** The "Library" view lists reports discovered from local search paths (e.g. `~/taminator-test-data`, `~/Documents/rh/customers`). Each entry can be viewed or opened in Google Docs.

## Security

- Client secret must not be committed to the repo. Use environment variables (e.g. `TAMINATOR_GOOGLE_CLIENT_ID`, `TAMINATOR_GOOGLE_CLIENT_SECRET`) or a local config file that is gitignored.
- Stored tokens should be in a restricted-permissions file or keyring.

## Files and config

- **Integration module:** `src/taminator/integrations/google_drive.py` (or similar) — OAuth2 flow, token load/save, Drive API calls.
- **Config:** Optional `~/.config/taminator/google_credentials.json` or env vars for client ID/secret; token in `google_token.json` or keyring under a Taminator key.
- **Web API:** `POST /api/google/create-doc` (body: `{ "customer": "wellsfargo" }` or `{ "content": "...", "title": "..." }`), returns `{ "url": "https://docs.google.com/..." }`.  
  `GET /api/library` returns `{ "accounts": [ { "customer": "...", "files": [ { "name": "...", "path": "...", "mtime": ... } ] } ] }`.  
  `GET /api/report?customer=wellsfargo` returns report content (or 404).

## References

- [Drive API: Create a file](https://developers.google.com/drive/api/guides/create-file)
- [Drive API: Python quickstart](https://developers.google.com/drive/api/quickstart/python)
- [OAuth 2.0 for Desktop apps](https://developers.google.com/identity/protocols/oauth2/native-app)
