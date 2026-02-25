#!/usr/bin/env bash
# Fix GitLab release asset links that use /release/ (404) instead of /releases/
# Usage: GITLAB_TOKEN=xxx ./scripts/fix-release-asset-link-typo.sh [v2.1.3]
# Default tag: v2.1.3
set -e
TAG="${1:-v2.1.3}"
PROJECT_ID=149753
BASE_URL="https://gitlab.cee.redhat.com/api/v4/projects/${PROJECT_ID}/releases/${TAG}/assets/links"

if [ -z "$GITLAB_TOKEN" ]; then
  echo "Set GITLAB_TOKEN and run again."
  exit 1
fi

echo "Listing asset links for ${TAG}..."
LINKS=$(curl -s -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" "$BASE_URL")
if echo "$LINKS" | jq -e '.[]' >/dev/null 2>&1; then
  for row in $(echo "$LINKS" | jq -c '.[]'); do
    id=$(echo "$row" | jq -r '.id')
    name=$(echo "$row" | jq -r '.name')
    url=$(echo "$row" | jq -r '.url')
    if echo "$url" | grep -q '/release/'; then
      new_url="${url//\/release\//\/releases\/}"
      echo "Fixing link id=$id '$name': $url -> $new_url"
      curl -s -o /dev/null -w "%{http_code}" --request PUT \
        -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
        --data-urlencode "url=${new_url}" \
        "${BASE_URL}/${id}"
      echo ""
    fi
  done
  echo "Done. Check: https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/${TAG}"
else
  echo "No links found or API error. Response: $LINKS"
fi
