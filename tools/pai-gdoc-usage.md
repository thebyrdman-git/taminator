# PAI-GDOC Tool Usage Documentation

## Overview
The `pai-gdoc` tool is specifically designed for accessing individual Google Docs, Sheets, and Slides URLs directly. It extracts content from specific documents when provided with exact URLs.

## Important Distinction
- **pai-gdoc**: Access specific Google Doc URLs (THIS IS THE CORRECT TOOL)
- **pai-gdocs-query**: Search across multiple Google Docs (NOT for specific URLs)
- **pai-gdocs-sync**: Sync Google Docs for search (NOT for specific URLs)

## Command Syntax
```bash
pai-gdoc <URL> [command] [options]
```

## Common Usage Examples

### Extract Document Content (Default)
```bash
pai-gdoc "https://docs.google.com/document/d/1MDjQy6E7zJ5b7rUKFVnDFwhiNweZRMkfyVivdAOt6dU/edit?usp=sharing"
```

### Extract in Markdown Format (Recommended)
```bash
pai-gdoc "https://docs.google.com/document/d/1MDjQy6E7zJ5b7rUKFVnDFwhiNweZRMkfyVivdAOt6dU/edit?usp=sharing" --format markdown
```

### Extract Content Only (No Metadata)
```bash
pai-gdoc "https://docs.google.com/document/d/1MDjQy6E7zJ5b7rUKFVnDFwhiNweZRMkfyVivdAOt6dU/edit?usp=sharing" --extract-only
```

### Get Document Metadata
```bash
pai-gdoc "https://docs.google.com/document/d/1MDjQy6E7zJ5b7rUKFVnDFwhiNweZRMkfyVivdAOt6dU/edit?usp=sharing" metadata
```

## Workflow Integration
When you have a specific Google Docs URL:

1. **Always use pai-gdoc** (not pai-gdocs-query or pai-gdocs-sync)
2. **Use --format markdown** for best readability
3. **Quote the URL** to handle special characters properly
4. **Save output to files** if content needs to be referenced later

## Supported URL Types
- Google Docs: `https://docs.google.com/document/d/...`
- Google Sheets: `https://docs.google.com/spreadsheets/d/...`
- Google Slides: `https://docs.google.com/presentation/d/...`

## Common Mistakes to Avoid
- ❌ Using pai-gdocs-query for specific URLs
- ❌ Using pai-gdocs-sync for specific URLs  
- ❌ Not quoting URLs with special characters
- ❌ Assuming search tools work with direct URLs

## Authentication
Uses existing Google OAuth credentials configured for PAI tools. If authentication fails, run:
```bash
pai-gdocs-query setup
```

This ensures consistent access to Google Workspace documents across PAI tools.