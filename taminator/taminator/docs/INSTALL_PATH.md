# Taminator install path

Use the same path on both Linux and Mac so scripts and docs stay consistent.

**Recommended install (repo) path:** `~/taminator`

- **Mac:** `/Users/<username>/taminator` (e.g. `/Users/jbyrd/taminator`)
- **Linux:** `/home/<username>/taminator` (e.g. `/home/jbyrd/taminator`)

Clone the repo so that the project root is that directory:

```bash
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git ~/taminator
```

The app (CLI and web UI) lives in the inner `taminator` directory. Run commands from there:

```bash
cd ~/taminator/taminator
./tam-rfe serve
./tam-rfe check wellsfargo
```

So on Mac you work in `/Users/jbyrd/taminator/taminator`, and on Linux in `/home/jbyrd/taminator/taminator` (or your username).
