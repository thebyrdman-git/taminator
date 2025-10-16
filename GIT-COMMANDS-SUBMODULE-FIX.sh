#!/bin/bash
# Git commands for rhcase submodule detection bug fix merge request
# Run these commands in order from the rfe-automation-clean directory

# Change to the project directory
cd /home/jbyrd/pai/rfe-automation-clean

# Create and checkout new branch for submodule bug fix
git checkout -b bugfix/rhcase-submodule-detection

# Stage the bug fix changes
git add install-improved.sh
git add DANIEL-ISSUE-RESPONSE.md
git add MERGE-REQUEST-SUBMODULE-FIX.md
git add GIT-COMMANDS-SUBMODULE-FIX.sh

# Commit with descriptive message
git commit -m "fix: Handle rhcase as git submodule in installer

Problem:
- Installer checked for rhcase using [ -d .git ] which fails for submodules
- In submodules, .git is a FILE (not directory) containing gitdir: path
- Caused 'Failed to clone rhcase' errors even with valid VPN access
- Blocked installation for users with existing repositories

Solution:
- Replace simple directory check with 'git rev-parse --git-dir'
- Detect and handle detached HEAD state (common in submodules)
- Use fetch + reset for detached HEAD instead of pull
- Clean up corrupted directories automatically
- Show detailed git error output for debugging

Testing:
- Fresh installation (no rhcase directory)
- Regular git repository (normal updates via pull)
- Git submodule with detached HEAD (fetch + reset)
- Corrupted directory (remove and reclone)

Fixes #2 reported by dwhitley (Daniel Whitley).
"

# Push branch to GitLab
git push -u origin bugfix/rhcase-submodule-detection

# After pushing, create merge request via GitLab web UI:
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/merge_requests/new"
echo ""
echo "2. Select:"
echo "   Source branch: bugfix/rhcase-submodule-detection"
echo "   Target branch: main"
echo ""
echo "3. Use this title:"
echo "   fix: Handle rhcase as git submodule in installer"
echo ""
echo "4. Copy merge request description from:"
echo "   MERGE-REQUEST-SUBMODULE-FIX.md"
echo ""
echo "5. Add labels: bug, priority::high, installer"
echo ""
echo "6. Reference: Fixes #2"
echo ""
echo "7. Submit merge request"
echo ""
echo "========================================"
echo ""
echo "Note: This is a high-priority bug fix that should be merged quickly"
echo ""

# Alternative: Create MR via glab CLI (if installed and configured)
# Uncomment these lines if you have glab installed:
#
# glab mr create \
#   --source-branch bugfix/rhcase-submodule-detection \
#   --target-branch main \
#   --title "fix: Handle rhcase as git submodule in installer" \
#   --description "$(cat MERGE-REQUEST-SUBMODULE-FIX.md)" \
#   --label "bug,priority::high,installer" \
#   --assignee @jbyrd \
#   --milestone "v1.0"

