# Pre-announce checklist — Taminator v2.0.0 tech preview

Use this before announcing the tech preview to coworkers.

---

## 1. Create the release (so downloads exist)

Tag and push so the pipeline runs and the GitLab release page has the AppImage links:

```bash
cd /Users/jbyrd/taminator
git tag v2.0.0
git push https://oauth2:${GITLAB_TOKEN}@gitlab.cee.redhat.com/jbyrd/taminator.git v2.0.0
```

Wait for the pipeline to pass. Then check: https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases — the v2.0.0 release should list the Linux x86_64 and ARM64 AppImage download links.

---

## 2. Quick link check

- **Releases:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- **User guide:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/USER-GUIDE.md
- **Issues (feedback):** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues

---

## 3. Announcement (optional template)

You can adapt this for Slack, email, or Confluence:

**Subject/headline:** Taminator v2.0.0 tech preview — RFE/bug report tool for TAMs

**Short blurb:**  
Taminator is a tool for generating and maintaining RFE and bug reports. It saves 2–3 hours per customer per week. We’re sharing a **tech preview** and would like your feedback.

- **Download (Linux):** [GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases) — AppImage for x86_64 and ARM64. Double-click to run; no terminal needed.
- **From repo:** `git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git ~/taminator` then `cd taminator/taminator && ./tam-rfe serve` for the browser UI.
- **Docs:** [User guide](https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/USER-GUIDE.md) on GitLab.
- **Feedback:** [GitLab issues](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues) (bugs, feature ideas, “I wish it did X”).

Requires Red Hat VPN and GitLab CEE access.

---

## 4. Done?

- [ ] Tag v2.0.0 pushed and pipeline passed
- [ ] Release page shows v2.0.0 with download links
- [ ] Announcement sent (Slack / email / etc.)
- [ ] Feedback channel (GitLab issues) is clear in the announcement
