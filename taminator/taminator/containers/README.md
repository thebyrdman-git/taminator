# Taminator container images

## RPM builder (Linux RPM on Mac via Podman)

Builds Taminator's Linux RPM inside a Fedora container so you can produce `.rpm` artifacts on a Mac.

### Prerequisites

- **Podman** on macOS (`brew install podman`), with a running machine:
  ```bash
  podman machine init    # if you haven't yet
  podman machine start
  ```

### Build the image

From **redhat/taminator/taminator** (the directory that contains `gui/` and `containers/`):

```bash
# Native arm64 (recommended on Apple Silicon; produces aarch64 RPM)
podman build --platform linux/arm64 -f containers/Containerfile.rpm -t taminator-rpm-builder .
```

### Run the RPM build

From the same directory (**redhat/taminator/taminator**):

```bash
podman run --rm -v "$(pwd):/app:z" -w /app/gui taminator-rpm-builder ./build-rpm.sh
```

Output RPM(s) will be under **gui/dist/** (e.g. `taminator-gui-2.0.0.aarch64.rpm` on Apple Silicon; the image is built for arm64 by default).

### Optional: shell inside the image

```bash
podman run --rm -it -v "$(pwd):/app:z" -w /app/gui taminator-rpm-builder bash
# then: npm ci && npx electron-builder --linux rpm
```
