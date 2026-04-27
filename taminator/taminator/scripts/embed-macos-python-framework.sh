#!/usr/bin/env bash
# Make python-bundle/bin/python self-contained for shipping in Taminator.app (arm64 and x64).
# Copies any referenced Python.framework from otool(1) and rewrites load paths to @loader_path/...
# so end users do not need /Library/Frameworks (python.org) or Homebrew in fixed paths.
set -euo pipefail
BUNDLE="${1:?usage: embed-macos-python-framework.sh <python-bundle-dir>}"
PY="${BUNDLE}/bin/python"
test -x "$PY" || { echo "not executable: $PY" >&2; exit 1; }

mkdir -p "${BUNDLE}/Frameworks" "${BUNDLE}/lib"

while IFS= read -r line; do
  first=$(echo "$line" | awk '{print $1}')
  case "$first" in
    ""|@*) continue ;;
    /usr/*|/System/*) continue ;;
  esac
  old=$first
  if [[ -f "$old" && "$old" == *Python.framework* ]]; then
    froot=$(echo "$old" | sed -n 's#\(.*Python\.framework\)/.*#\1#p')
    if [[ -z "$froot" || ! -d "$froot" ]]; then
      continue
    fi
    if [[ ! -d "$BUNDLE/Frameworks/Python.framework" ]]; then
      echo "Copying $froot -> $BUNDLE/Frameworks/"
      cp -R "$froot" "$BUNDLE/Frameworks/"
    fi
    if [[ -d "$BUNDLE/Frameworks/Python.framework" ]]; then
      suffix="${old#*Python.framework}"
      new="@loader_path/../Frameworks/Python.framework${suffix}"
      if [[ "$old" != "$new" ]]; then
        echo "install_name_tool: $old -> $new"
        install_name_tool -change "$old" "$new" "$PY" 2>/dev/null || true
      fi
    fi
  elif [[ -f "$old" && ( "$old" == *.dylib || "$old" == *libpython* ) ]]; then
    base=$(basename "$old")
    if [[ ! -f "$BUNDLE/lib/$base" ]]; then
      echo "Copying $old -> $BUNDLE/lib/"
      cp -a "$old" "$BUNDLE/lib/"
    fi
    if [[ -f "$BUNDLE/lib/$base" ]]; then
      new="@loader_path/../lib/$base"
      echo "install_name_tool: $old -> $new"
      install_name_tool -change "$old" "$new" "$PY" 2>/dev/null || true
    fi
  fi
done < <(otool -L "$PY" | tail -n +2)

echo "Verifying: $PY"
"$PY" -c "import encodings, rich; print('embed-macos-python-framework: ok')"
