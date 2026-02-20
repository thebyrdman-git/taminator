# Release asset URL pattern

**Correct path (files in repo under `releases/<tag>/`):**

```
https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/<tag>/<filename>
```

Use **`releases`** (plural). Using **`release`** (singular) returns 404.

Examples:
- Correct: `.../raw/main/releases/v2.1.3/Taminator-2.1.3.AppImage`
- Wrong (404): `.../raw/main/release/v2.1.3/Taminator-2.1.3.AppImage`

When adding asset links to a GitLab release (Releases → Edit), use the correct URL above.
