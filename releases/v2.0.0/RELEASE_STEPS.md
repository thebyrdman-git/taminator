# Release steps for v2.0.0

Use these steps from the **taminator repo** (the one you push to GitLab).

## Prerequisites

- Main branch pushed and pipeline green.
- For tagging: `GITLAB_TOKEN` in your environment (e.g. from `~/.zshrc`).
- For releases/ dir in repo: in GitLab go to Settings → CI/CD → Variables and add `GITLAB_TOKEN` (or create a project token with `write_repository`) so the `release:copy-to-repo` job can push the built AppImages into `releases/<tag>/`.

## 1. Tag and push

From the taminator repo root (e.g. `/Users/jbyrd/taminator`):

```bash
cd /path/to/taminator   # repo root, not taminator/taminator
git tag v2.0.0
git push https://oauth2:${GITLAB_TOKEN}@gitlab.cee.redhat.com/jbyrd/taminator.git v2.0.0
```

## 2. What happens

- Pipeline runs on tag `v2.0.0`: `build:linux:x64` and `build:linux:arm64` build the AppImages.
- When both succeed, `release:gitlab` creates the GitLab release and attaches the two download links.
- If `GITLAB_TOKEN` is set in CI/CD variables with write access, `release:copy-to-repo` copies the AppImages into `releases/v2.0.0/` in the repo and pushes to the default branch, so the files are available in the tree (clone or browse).

## 3. After release

- **Releases page:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- **Pipelines:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

If you need to re-run or fix the release, delete the tag locally and on GitLab, fix, then re-tag and push again.
