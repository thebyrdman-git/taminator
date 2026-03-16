# Building Taminator GUI

## Local builds

From this directory (`taminator/gui`):

```bash
npm install
npm run build:mac      # macOS DMG (x64 + arm64)
npm run build:linux:appimage
```

Output is in `dist/` (and often copied to `../../artifacts/`).

## macOS code signing

**Current DMGs are not code-signed.** There is no `_CodeSignature` (or `CodeResources`) in the app bundle because the build did not find a valid **Developer ID Application** identity. That is expected when no Apple Developer ID cert is installed.

To produce a **signed** Mac app and DMG:

1. **Get a certificate:** Apple Developer Program → Certificates → create a **Developer ID Application** certificate. Install it in your Keychain.

2. **Build with signing:** Either let electron-builder auto-detect the identity, or set it explicitly:

   ```bash
   # Use a specific identity (list with: security find-identity -v -p codesigning)
   export CSC_NAME="Developer ID Application: Your Name (TEAMID)"
   npm run build:mac
   ```

   Or in `package.json` under `build.mac` add:

   ```json
   "identity": "Developer ID Application: Your Name (TEAMID)"
   ```

3. **Sign an already-built app:** Use the **unpacked** app from `dist/` (not the mounted DMG). Mounted DMGs are read-only, so you can’t sign the app in place; you must sign the unpacked app, then repack a new DMG.

   **Option A – script (signs both arches and repacks):**
   ```bash
   export CSC_NAME="Developer ID Application: Your Name (TEAMID)"
   ./sign-and-repack-dmg.sh
   ```

   **Option B – manual:**
   ```bash
   APP=dist/mac-arm64/Taminator.app   # or dist/mac/Taminator.app for x64
   codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" "$APP"
   hdiutil create -volname Taminator -srcfolder dist/mac-arm64 -ov -format UDZO Taminator-2.1.6-arm64-signed.dmg
   ```

   Sign in `dist/mac-arm64/` (or `dist/mac/`), then repack the DMG from that folder.

## Notarization (optional)

For distribution outside the Mac App Store, notarization is recommended after signing. Set `CSC_LINK` (path to your .p12) and `CSC_KEY_PASSWORD`, and use an `afterSign` hook to run `xcrun notarytool` or the legacy `altool`; see [electron-builder code signing](https://www.electron.build/code-signing).
