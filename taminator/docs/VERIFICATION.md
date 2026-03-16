# Verification and CI/CD

We run the same checks locally and in CI so you can have full confidence in what you ship.

## What runs where

| Check | Local | CI (on tag push) |
|-------|--------|-------------------|
| Icon exists (`taminator/gui/build/icon.png`) | `scripts/verify.sh` | `verify` job |
| GUI ESLint | `cd taminator/gui && npm run lint` | `verify` job |
| Python / tam-rfe smoke | `scripts/verify.sh` (skip with `--no-python`) | Optional in verify |
| Electron build | `cd taminator/gui && npm run build:mac` etc. | `build` job (after verify) |

## Before you push or tag

From the repo root:

```bash
./scripts/verify.sh
```

If everything passes, CI will pass the same checks. The build job only runs after the verify job succeeds.

## In Cursor / your editor

- **ESLint:** Install the ESLint extension and open `taminator/gui` so you see lint results in the editor.
- **Run verify:** Use the terminal or add a task (e.g. in VS Code/Cursor: Run Task → "Verify") that runs `./scripts/verify.sh`.
- **Cursor rule:** The rule in `.cursor/rules/verification.mdc` reminds the AI to run verify before suggesting a push or tag.

## Adding more checks

To add a new check:

1. Add it to `scripts/verify.sh` so local and CI stay in sync.
2. If it belongs in the `verify` job, add a step in `.github/workflows/electron-build.yml` in the `verify` job (or call `scripts/verify.sh` there; the job already runs it with `--no-python`).
3. Keep the verify script fast so it stays practical to run before every push.
