# Running the Taminator AppImage on Fedora (x64 or ARM64)

## No FUSE? Use the launcher script (automated)

Each Linux artifact (x64 and ARM64) includes **run-taminator-no-fuse.sh** next to the AppImage. It runs the AppImage with `--appimage-extract-and-run` so **FUSE is not required**. Use it if you haven't installed `fuse` or if the AppImage fails to mount:

```bash
chmod +x run-taminator-no-fuse.sh
./run-taminator-no-fuse.sh
```

Keep the script in the same directory as the `.AppImage` file.

---

## Use the right build for your CPU

- **x86_64 / amd64 Fedora** → download artifact **taminator-Linux-&lt;ref&gt;** (e.g. `taminator-Linux-main`). The AppImage inside is x64.
- **aarch64 / ARM64 Fedora** (e.g. Apple Silicon VM, Graviton, RPi) → download artifact **taminator-Linux-arm64-&lt;ref&gt;** (e.g. `taminator-Linux-arm64-main`). The AppImage inside is arm64.

If you use the x64 AppImage on an ARM64 machine (or the other way around), it will not launch (wrong architecture).

---

## Steps to run on Fedora

1. **Install FUSE (required for AppImage)**  
   ```bash
   sudo dnf install fuse
   ```
   If the AppImage still won’t run, try:
   ```bash
   sudo dnf install fuse3
   ```

2. **Make the AppImage executable**  
   ```bash
   chmod +x Taminator-*.AppImage
   ```

3. **Run from the terminal (so you see errors and debug output)**  
   ```bash
   ./Taminator-2.1.6.AppImage
   ```
   If the app fails to start the server, you’ll see:
   - Console output: `[Main] Server startup debug:` and any `[Server stderr]` / `[Server stdout]`
   - An error window with debug info
   - A debug file: `~/.config/taminator-gui/server-startup-debug.txt`

4. **If it still doesn’t launch (no window at all)**  
   - Try extracting and running (avoids FUSE):  
     ```bash
     ./Taminator-*.AppImage --appimage-extract-and-run
     ```
   - Or extract once and run the binary:  
     ```bash
     ./Taminator-*.AppImage --appimage-extract
     ./squashfs-root/AppRun
     ```

5. **Check architecture**  
   ```bash
   uname -m
   file ./Taminator-*.AppImage
   ```
   - `uname -m` should be `aarch64` on ARM64 Fedora.
   - `file` should show something like `... ARM aarch64 ...` for the ARM64 AppImage, or `... x86-64 ...` for the x64 one.

---

## If the ARM64 artifact is missing or build failed

The workflow job **Build Linux ARM64 (AppImage)** has `continue-on-error: true`, so the rest of the workflow can succeed even if the ARM64 build fails. Check the Actions run:

- Open the workflow run → **Build Linux ARM64 (AppImage)**.
- If the job is red/failed, open the logs to see why (e.g. QEMU, npm, or electron-builder errors).
- You can build the ARM64 AppImage locally on an ARM64 machine:
  ```bash
  cd taminator/gui
  npm ci
  npx electron-builder --linux AppImage --arm64 --publish never
  ```
  The output will be in `dist/`.
