#!/bin/bash
# Create GitLab release via API

set -e  # Exit on error
# set -x  # Uncomment for full debug output

GITLAB_TOKEN="${GITLAB_TOKEN:?Set GITLAB_TOKEN environment variable}"
GITLAB_URL="https://gitlab.cee.redhat.com"
VERSION="1.9.2"
TAG_NAME="v1.9.2"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   🚀 CREATE GITLAB RELEASE VIA API                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Get project ID
echo "Step 1: Getting project ID..."
PROJECT_ID=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/jbyrd%2Ftaminator" | \
  grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Could not get project ID"
    exit 1
fi

echo "✅ Project ID: $PROJECT_ID"
echo ""

# Create tag first (required for release)
echo "Step 2: Creating tag $TAG_NAME..."
TAG_RESPONSE=$(curl -w "\nHTTP_STATUS:%{http_code}" --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{
    \"tag_name\": \"$TAG_NAME\",
    \"ref\": \"main\",
    \"message\": \"Release $TAG_NAME\"
  }" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/tags")

HTTP_STATUS=$(echo "$TAG_RESPONSE" | grep HTTP_STATUS | cut -d: -f2)
TAG_BODY=$(echo "$TAG_RESPONSE" | sed '/HTTP_STATUS/d')

if [ "$HTTP_STATUS" = "201" ] || [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Tag created (HTTP $HTTP_STATUS)"
elif echo "$TAG_BODY" | grep -q "already exists"; then
    echo "⚠️  Tag already exists, continuing..."
else
    echo "❌ Tag creation failed (HTTP $HTTP_STATUS)"
    echo "Response: $TAG_BODY"
    exit 1
fi
echo ""

# Create release notes JSON
echo "Step 3: Creating release..."

RELEASE_NOTES=$(cat <<'EOF'
## Taminator v1.9.2 - Production Release

### 🎉 What's New
- ✅ **Core stability improvements**
- ✅ **Setup wizard for first-time users**
- ✅ **Empty states with helpful guidance**
- ✅ **All core features fully functional**
- ✅ **Cross-platform release (Linux, macOS, Windows)**

### 📥 Downloads

**All files available via Git LFS:**
```bash
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator/releases/v1.9.2/
```

Files included:
- Linux AppImage (116 MB)
- macOS Universal DMG (111 MB)
- Windows Installer (88 MB)

### 🔧 Installation

**Linux:**
```bash
# Download Taminator-1.9.2.AppImage from assets below
chmod +x Taminator-1.9.2.AppImage
./Taminator-1.9.2.AppImage
```

### 🐛 Bug Fixes
- Fixed settings save functionality
- Fixed bug report submission
- Fixed T3/KAB tab visibility
- Removed hardcoded test data
- Improved error handling

### 🔒 Requirements
- Red Hat VPN for KB/T3 features
- Portal token (rh_jwt cookie) for authentication
- JIRA token for RFE tracking

### 📚 Documentation
- [README](https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/README.md)
- [Getting Started Guide](https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/GETTING-STARTED.md)

---

**"Come with me if you want to save time."** - Taminator T-800
EOF
)

# Create the release with assets
RELEASE_RESPONSE=$(curl -w "\nHTTP_STATUS:%{http_code}" --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{
    \"name\": \"Taminator v1.9.2 - Cross-Platform Release\",
    \"tag_name\": \"$TAG_NAME\",
    \"description\": $(echo "$RELEASE_NOTES" | jq -Rs .),
    \"assets\": {
      \"links\": [
        {
          \"name\": \"📥 Release Files (Git LFS)\",
          \"url\": \"$GITLAB_URL/jbyrd/taminator/-/tree/main/releases/v1.9.2\",
          \"link_type\": \"other\"
        },
        {
          \"name\": \"📚 Getting Started Guide\",
          \"url\": \"$GITLAB_URL/jbyrd/taminator/-/blob/main/GETTING-STARTED.md\",
          \"link_type\": \"other\"
        },
        {
          \"name\": \"📖 Full Documentation\",
          \"url\": \"$GITLAB_URL/jbyrd/taminator/-/blob/main/README.md\",
          \"link_type\": \"other\"
        }
      ]
    }
  }" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/releases")

HTTP_STATUS=$(echo "$RELEASE_RESPONSE" | grep HTTP_STATUS | cut -d: -f2)
RELEASE_BODY=$(echo "$RELEASE_RESPONSE" | sed '/HTTP_STATUS/d')

echo ""
if [ "$HTTP_STATUS" = "201" ] || [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Release created successfully! (HTTP $HTTP_STATUS)"
    echo ""
    echo "View release at:"
    echo "  $GITLAB_URL/jbyrd/taminator/-/releases/$TAG_NAME"
    echo ""
else
    echo "❌ Release creation failed (HTTP $HTTP_STATUS)"
    echo ""
    echo "API Response:"
    echo "$RELEASE_BODY" | jq '.' 2>/dev/null || echo "$RELEASE_BODY"
    echo ""
    exit 1
fi

