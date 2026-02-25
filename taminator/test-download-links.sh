#!/bin/bash
# Test script to verify Taminator download links work
# Run this BEFORE committing README changes

set -e

GITLAB_TOKEN="${GITLAB_TOKEN:-$(cat ~/.config/pai/secrets/gitlab-token 2>/dev/null)}"

if [ -z "$GITLAB_TOKEN" ]; then
    echo "❌ GITLAB_TOKEN not set and not found in ~/.config/pai/secrets/gitlab-token"
    exit 1
fi

echo "🧪 Testing Taminator Download Links"
echo "===================================="
echo ""

PROJECT_URL="https://gitlab.cee.redhat.com/jbyrd/taminator"
FILES=(
    "Taminator-1.7.0.AppImage"
    "Taminator-1.7.0.dmg"
    "Taminator-1.7.0-arm64.dmg"
    "Taminator_Setup_1.7.0.exe"
)

# Test 1: Check if files exist in repo
echo "📋 Test 1: Files exist in repository"
echo "-------------------------------------"
for file in "${FILES[@]}"; do
    echo -n "Checking $file... "
    if git ls-tree HEAD | grep -q "$file"; then
        echo "✅ Found in git"
    else
        echo "❌ NOT in git"
        exit 1
    fi
done
echo ""

# Test 2: Test /raw/ endpoint (should redirect to login - expected behavior for GitLab CEE)
echo "📋 Test 2: Raw endpoint accessibility"
echo "--------------------------------------"
for file in "${FILES[@]}"; do
    URL="https://oauth2:${GITLAB_TOKEN}@${PROJECT_URL##https://}/-/raw/main/$file"
    echo -n "Testing $file... "
    
    RESPONSE=$(curl -s -L -w "%{http_code}|%{content_type}|%{size_download}" -o /dev/null "$URL")
    HTTP_CODE=$(echo "$RESPONSE" | cut -d'|' -f1)
    CONTENT_TYPE=$(echo "$RESPONSE" | cut -d'|' -f2)
    SIZE=$(echo "$RESPONSE" | cut -d'|' -f3)
    
    if [ "$HTTP_CODE" = "200" ] && [ "$CONTENT_TYPE" = "text/html; charset=utf-8" ] && [ "$SIZE" -lt "20000" ]; then
        echo "⚠️  Redirects to login (expected for GitLab CEE)"
    elif [ "$HTTP_CODE" = "200" ] && [ "$SIZE" -gt "1000000" ]; then
        echo "✅ Downloads directly (unexpected but good!)"
    else
        echo "❌ HTTP $HTTP_CODE, Size: $SIZE"
        exit 1
    fi
done
echo ""

# Test 3: Verify GitLab web UI links work
echo "📋 Test 3: GitLab project accessibility"
echo "----------------------------------------"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${PROJECT_URL}")
if [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Project page accessible (redirects to login or shows content)"
else
    echo "❌ Project page returned HTTP $HTTP_CODE"
    exit 1
fi
echo ""

# Summary
echo "📊 Summary"
echo "----------"
echo "✅ All files present in repository"
echo "⚠️  Direct downloads require browser login (GitLab CEE security)"
echo "✅ Project accessible at: $PROJECT_URL"
echo ""
echo "📖 Documentation should instruct users to:"
echo "   1. Connect to Red Hat VPN"
echo "   2. Visit project page in browser"
echo "   3. Click on file name"
echo "   4. Click 'Download' button"
echo ""
echo "✅ All tests passed!"

