# GitHub Actions CI/CD

## Workflows

### 1. CI (`ci.yml`)
Runs on every push and pull request to `main` or `develop` branches.

**Jobs:**
- `lint-python`: Validates Python code with flake8
- `test-gui`: Tests GUI build and validates package.json
- `security-scan`: Checks for hardcoded secrets and customer data

### 2. Release (`release.yml`)
Builds cross-platform releases for Windows and macOS.

**Triggers:**
- Git tag push: `git push origin v1.9.2`
- Manual dispatch: GitHub UI > Actions > "Build and Release" > Run workflow

**Jobs:**
- `build-windows`: Creates Windows NSIS installer on Windows runner
- `build-macos`: Creates macOS DMG (Intel + Apple Silicon) on macOS runner
- `create-release`: Publishes GitHub release with all artifacts

## Running a Release Build

### Option 1: Tag-based (Recommended)
```bash
cd /home/jbyrd/pai/taminator
git tag v1.9.2
git push github v1.9.2
```

### Option 2: Manual Dispatch
1. Go to: https://github.com/thebyrdman-git/taminator/actions
2. Click "Build and Release" workflow
3. Click "Run workflow"
4. Enter version (e.g., `v1.9.2`)
5. Click "Run workflow" button

## Monitoring Builds
- View progress: https://github.com/thebyrdman-git/taminator/actions
- Download artifacts: Available for 7 days after build
- Release page: https://github.com/thebyrdman-git/taminator/releases

## Build Times (Approximate)
- Windows: ~10-15 minutes
- macOS: ~15-20 minutes
- Total pipeline: ~25-30 minutes

## Artifacts Produced
- `Taminator-Setup-1.9.2.exe` (Windows NSIS installer)
- `Taminator-1.9.2-x64.dmg` (macOS Intel)
- `Taminator-1.9.2-arm64.dmg` (macOS Apple Silicon)

## Troubleshooting

### Build fails on Windows
- Check Node.js version (requires 20+)
- Verify `gui/package-lock.json` exists
- Check electron-builder Windows dependencies

### Build fails on macOS
- Check Xcode Command Line Tools installed on runner
- Verify macOS signing/notarization settings (currently unsigned)
- Check disk space on runner

### Release not created
- Verify `GITHUB_TOKEN` has `contents: write` permission
- Check that tag exists: `git tag -l v1.9.2`
- Verify both build jobs completed successfully

## Security Notes
- No secrets required for unsigned builds
- `GITHUB_TOKEN` automatically provided by GitHub Actions
- Customer data checks run on every commit
- Hardcoded token scanning prevents leaks

## Future Enhancements
- [ ] Code signing for Windows (requires certificate)
- [ ] Notarization for macOS (requires Apple Developer account)
- [ ] Linux builds on GitHub Actions
- [ ] Automated version bumping
- [ ] Changelog generation from git commits

