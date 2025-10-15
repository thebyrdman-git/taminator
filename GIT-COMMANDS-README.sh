#!/bin/bash
# Git commands for README update merge request
# Run these commands in order from the rfe-automation-clean directory

# Change to the project directory
cd /home/jbyrd/pai/rfe-automation-clean

# Create and checkout new branch for README updates
git checkout -b feature/update-readme-automated-installer

# Stage the README changes
git add README.md
git add README-UPDATES.md
git add MERGE-REQUEST-README-UPDATE.md
git add GIT-COMMANDS-README.sh

# Commit with descriptive message
git commit -m "docs: Update README to reflect automated installer

- Update Quick Start with 3-command installation
- Simplify requirements to minimal essentials (git + python3)
- Replace install-dependencies with install-improved.sh
- Highlight automation features (no sudo, smart fallback, auto-clones rhcase)
- Modernize Get the Tool section (git clone primary, ZIP alternative)
- Add installation time estimate (2-5 minutes)
- Emphasize 'no dependency hell' approach

Related to automated installer implementation.
"

# Push branch to GitLab
git push -u origin feature/update-readme-automated-installer

# After pushing, create merge request via GitLab web UI:
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/merge_requests/new"
echo ""
echo "2. Select:"
echo "   Source branch: feature/update-readme-automated-installer"
echo "   Target branch: main"
echo ""
echo "3. Use this title:"
echo "   docs: Update README to reflect automated installer"
echo ""
echo "4. Copy merge request description from:"
echo "   MERGE-REQUEST-README-UPDATE.md"
echo ""
echo "5. Add labels: documentation, enhancement"
echo ""
echo "6. Submit merge request"
echo ""
echo "========================================"
echo ""
echo "Note: This MR should be merged AFTER the automated installer MR"
echo ""

# Alternative: Create MR via glab CLI (if installed and configured)
# Uncomment these lines if you have glab installed:
#
# glab mr create \
#   --source-branch feature/update-readme-automated-installer \
#   --target-branch main \
#   --title "docs: Update README to reflect automated installer" \
#   --description "$(cat MERGE-REQUEST-README-UPDATE.md)" \
#   --label "documentation,enhancement" \
#   --assignee @jbyrd

