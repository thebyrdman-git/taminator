#!/bin/bash
# Create GitLab release v2.1.5 via API (tag + description + asset links)
# Usage: GITLAB_TOKEN=your_token ./create-gitlab-release-2.1.5.sh
#   or:  ./create-gitlab-release-2.1.5.sh your_token

set -e

if [ -n "$1" ]; then
  GITLAB_TOKEN="$1"
fi
GITLAB_TOKEN="${GITLAB_TOKEN:?Set GITLAB_TOKEN environment variable or pass as first argument}"
GITLAB_URL="https://gitlab.cee.redhat.com"
TAG_NAME="v2.1.5"

echo "Creating GitLab release $TAG_NAME..."

PROJECT_ID=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/jbyrd%2Ftaminator" | \
  grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)

if [ -z "$PROJECT_ID" ]; then
  echo "Could not get project ID"
  exit 1
fi

# Create tag
TAG_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"tag_name\": \"$TAG_NAME\", \"ref\": \"main\", \"message\": \"Release $TAG_NAME\"}" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/tags")

HTTP_STATUS=$(echo "$TAG_RESPONSE" | grep HTTP_STATUS | cut -d: -f2)
TAG_BODY=$(echo "$TAG_RESPONSE" | sed '/HTTP_STATUS/d')

if [ "$HTTP_STATUS" = "201" ] || [ "$HTTP_STATUS" = "200" ]; then
  echo "Tag $TAG_NAME created"
elif echo "$TAG_BODY" | grep -q "already exists"; then
  echo "Tag $TAG_NAME already exists, continuing..."
else
  echo "Tag creation failed (HTTP $HTTP_STATUS): $TAG_BODY"
  exit 1
fi

# Release description and asset links (raw download URLs)
DESC="## Taminator v2.1.5

### Downloads
- [Taminator-2.1.5.dmg](https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.5/Taminator-2.1.5.dmg) — macOS Intel x64
- [Taminator-2.1.5-arm64.dmg](https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.5/Taminator-2.1.5-arm64.dmg) — macOS Apple Silicon
- [Taminator-2.1.5.AppImage](https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.5/Taminator-2.1.5.AppImage) — Linux x64

### Fix notes (v2.1.5)
- App version now shown in the UI (hero). Electron passes version to server (TAMINATOR_APP_VERSION).
- JIRA clone/backport links in Check and Update.
- Build/release: validate job, optional GitHub Release, build-from-commit logging.
"

# Build JSON: description + assets.links for each file
LINKS_JSON='[
  {"name": "Taminator-2.1.5.dmg (macOS Intel)", "url": "https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.5/Taminator-2.1.5.dmg", "link_type": "package"},
  {"name": "Taminator-2.1.5-arm64.dmg (macOS Apple Silicon)", "url": "https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.5/Taminator-2.1.5-arm64.dmg", "link_type": "package"},
  {"name": "Taminator-2.1.5.AppImage (Linux x64)", "url": "https://gitlab.cee.redhat.com/jbyrd/taminator/-/raw/main/releases/v2.1.5/Taminator-2.1.5.AppImage", "link_type": "package"}
]'
DESC_ESC=$(echo "$DESC" | jq -Rs .)

RELEASE_JSON=$(jq -n \
  --arg name "Taminator v2.1.5" \
  --arg tag "$TAG_NAME" \
  --argjson desc "$DESC_ESC" \
  --argjson links "$LINKS_JSON" \
  '{name: $name, tag_name: $tag, description: $desc, assets: { links: $links }}')

RELEASE_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "$RELEASE_JSON" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/releases")

HTTP_STATUS=$(echo "$RELEASE_RESPONSE" | grep HTTP_STATUS | cut -d: -f2)
RELEASE_BODY=$(echo "$RELEASE_RESPONSE" | sed '/HTTP_STATUS/d')

if [ "$HTTP_STATUS" = "201" ] || [ "$HTTP_STATUS" = "200" ]; then
  echo "Release created: $GITLAB_URL/jbyrd/taminator/-/releases/$TAG_NAME"
else
  echo "Release creation failed (HTTP $HTTP_STATUS)"
  echo "$RELEASE_BODY" | jq '.' 2>/dev/null || echo "$RELEASE_BODY"
  exit 1
fi
