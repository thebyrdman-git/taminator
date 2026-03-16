# Hydra / Customer Portal API — token and edit notes

Technical notes from demo feedback (Lenny Shirley, Feb 2026). Use when implementing Portal/Hydra API properly.

---

## Hydra = Customer Portal API token

**Same credential.** The "Hydra" APIs (e.g. `https://access.redhat.com/hydra/rest/search/cases`, `/hydra/rest/v1/ping`) use the **Customer Portal API token** from https://access.redhat.com/management/api. There is no separate Hydra token for these access.redhat.com endpoints. In Taminator, discovery and portal posting both use this token (or Red Hat username/password as an alternative). The UI treats "Hydra" and "Portal" as one token for access.redhat.com. Auth was simplified: one Customer Portal token in Settings; config and vault map Hydra to the same credential; CLI config menu no longer offers a separate Hydra token.

---

## API token (access.redhat.com)

- **Where to get it:** https://access.redhat.com/management/api  
- **Token type:** **OFFLINE** token.  
  - In the app you use it to obtain a **REFRESH** token.  
  - **REFRESH** token: lasts **15 minutes**.  
  - **OFFLINE** token: expires after **30 days** if unused; can last indefinitely if used at least once every 30 days (to obtain a refresh token).

Implementation implication: use the OFFLINE token to get a short-lived REFRESH token for API calls; refresh when needed (e.g. when refresh token expires or before a session).

---

## Edit for Private Portal posts

- **EDIT** of existing Private Portal posts may be possible by specifying the **ID** of the object.  
- That ID would need to be obtained via **another API call** (e.g. GET the discussion/post first to get its ID, then use that ID in the edit request).  
- Not 100% confirmed; worth validating when implementing edit/update for portal discussions.

---

## Submitting more detail to GitLab

If you work up full technical details (endpoints, request/response shapes, refresh flow), you can submit them as a doc or issue to the Taminator GitLab repo so implementation stays aligned with Red Hat’s API behavior.
