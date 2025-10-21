# 🖼️ Feature: Portal Preview Sandbox

## 🎯 Purpose
Provide TAMs with a live preview of how their RFE/Bug reports will appear in the Red Hat Customer Portal before publishing. This ensures formatting, links, and styling are correct.

## 💡 User Story
**As a TAM**, I want to preview my report exactly as it will appear in the Customer Portal so that I can:
- Verify formatting and styling
- Test links and tables
- Catch errors before publishing
- Ensure professional appearance
- Save time on revisions

## 🎨 UI Design

### Report Generation with Preview
```
┌─────────────────────────────────────────────────────────────────┐
│ Generate Report for TD Bank                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────────────────────┐│
│  │ 📝 Edit            │  │ 🖼️ Preview (Portal View)          ││
│  ├────────────────────┤  ├────────────────────────────────────┤│
│  │                    │  │ ┌────────────────────────────────┐ ││
│  │ # TD Bank RFE/Bug  │  │ │  [Red Hat Logo]                │ ││
│  │ ## Summary         │  │ │                                │ ││
│  │ 9 total cases      │  │ │  TD Bank RFE/Bug Tracker       │ ││
│  │                    │  │ │  ─────────────────────────────│ ││
│  │ ## RFEs            │  │ │  Summary: 9 total cases       │ ││
│  │ - AAPRFE-762...    │  │ │  (7 RFE, 2 Bug)               │ ││
│  │                    │  │ │                                │ ││
│  │ ## Bugs            │  │ │  Enhancement Requests          │ ││
│  │ - AAP-53458...     │  │ │  [Table with styled links]    │ ││
│  │                    │  │ └────────────────────────────────┘ ││
│  │ [Live editing]     │  │                                    ││
│  │                    │  │  💡 Tip: Links are clickable!     ││
│  └────────────────────┘  └────────────────────────────────────┘│
│                                                                 │
│  Preview Options:                                               │
│  [Desktop View] [Mobile View] [Print View]                     │
│  [Export Screenshot] [Publish to Portal]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Split View Preview
```
┌─────────────────────────────────────────────────────────────────┐
│ ● ○ ○  TD Bank Report - Preview Mode               _ □ X       │
├─────────────────────────────────────────────────────────────────┤
│  50%  ││  50%                                                   │
│ ─────────────────────────────────────────────────────────────── │
│                                                                 │
│  MARKDOWN SOURCE     ││  PORTAL PREVIEW                        │
│  ─────────────────   ││  ────────────────                      │
│                      ││                                         │
│  # TD Bank           ││  ╔══════════════════════════════════╗  │
│  RFE/Bug Tracker     ││  ║  Red Hat Customer Portal         ║  │
│                      ││  ╠══════════════════════════════════╣  │
│  **Summary**: 9      ││  ║                                  ║  │
│  total cases         ││  ║  TD Bank RFE/Bug Tracker        ║  │
│  (7 RFE, 2 Bug)      ││  ║                                  ║  │
│                      ││  ║  Summary: 9 total cases          ║  │
│  ## RFEs             ││  ║  (7 RFE, 2 Bug)                  ║  │
│                      ││  ║                                  ║  │
│  | JIRA ID | ...     ││  ║  Enhancement Requests            ║  │
│  |---------|---      ││  ║  ┌──────────────────────────┐   ║  │
│  | AAPRFE-762 |...   ││  ║  │JIRA ID    │ Status       │   ║  │
│                      ││  ║  ├───────────┼──────────────┤   ║  │
│  ← Edit here         ││  ║  │AAPRFE-762 │ Backlog      │   ║  │
│                      ││  ║  └──────────────────────────┘   ║  │
│                      ││  ║                                  ║  │
│                      ││  ╚══════════════════════════════════╝  │
│                      ││                                         │
│                      ││  ← Looks like Portal!                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🎨 Red Hat Customer Portal Styling

### Portal CSS Emulation
```css
/* Red Hat Customer Portal Theme */
.portal-preview {
  font-family: 'Red Hat Text', 'RedHatText', 'Overpass', sans-serif;
  background: #FFFFFF;
  color: #151515;
  line-height: 1.5;
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Portal Headers */
.portal-preview h1 {
  font-size: 36px;
  font-weight: 700;
  color: #EE0000;
  margin-bottom: 24px;
  border-bottom: 2px solid #EE0000;
  padding-bottom: 12px;
}

.portal-preview h2 {
  font-size: 28px;
  font-weight: 600;
  color: #151515;
  margin-top: 32px;
  margin-bottom: 16px;
}

.portal-preview h3 {
  font-size: 22px;
  font-weight: 600;
  color: #151515;
  margin-top: 24px;
  margin-bottom: 12px;
}

/* Portal Tables */
.portal-preview table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.portal-preview th {
  background: #F5F5F5;
  color: #151515;
  font-weight: 600;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 2px solid #D2D2D2;
}

.portal-preview td {
  padding: 12px 16px;
  border-bottom: 1px solid #F0F0F0;
}

.portal-preview tr:hover {
  background: #F9F9F9;
}

/* Portal Links */
.portal-preview a {
  color: #0066CC;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.2s;
}

.portal-preview a:hover {
  border-bottom-color: #0066CC;
}

/* Portal Badges */
.portal-preview .badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.portal-preview .badge-success {
  background: #E7F8E7;
  color: #3E8635;
}

.portal-preview .badge-warning {
  background: #FFF8E6;
  color: #795600;
}

.portal-preview .badge-info {
  background: #E5F0FF;
  color: #0066CC;
}

/* Portal Code Blocks */
.portal-preview pre {
  background: #F5F5F5;
  border: 1px solid #D2D2D2;
  border-radius: 4px;
  padding: 16px;
  overflow-x: auto;
  font-family: 'Red Hat Mono', 'Courier New', monospace;
}

.portal-preview code {
  background: #F5F5F5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Red Hat Mono', 'Courier New', monospace;
  font-size: 14px;
}

/* Portal Lists */
.portal-preview ul, .portal-preview ol {
  margin: 16px 0;
  padding-left: 32px;
}

.portal-preview li {
  margin: 8px 0;
}

/* Portal Blockquotes */
.portal-preview blockquote {
  border-left: 4px solid #EE0000;
  padding-left: 16px;
  margin: 16px 0;
  color: #6A6E73;
  font-style: italic;
}
```

## 🔧 Implementation

### HTML Structure
```html
<!-- Add to index.html -->
<div id="portal-preview-modal" style="display: none;">
  <div class="preview-modal">
    <div class="preview-header">
      <h2>🖼️ Portal Preview: <span id="preview-customer-name"></span></h2>
      <button onclick="closePreview()">✕</button>
    </div>
    
    <div class="preview-toolbar">
      <button class="btn btn-secondary" onclick="setPreviewMode('desktop')">
        💻 Desktop
      </button>
      <button class="btn btn-secondary" onclick="setPreviewMode('mobile')">
        📱 Mobile
      </button>
      <button class="btn btn-secondary" onclick="exportPreviewScreenshot()">
        📸 Screenshot
      </button>
      <button class="btn btn-primary" onclick="publishFromPreview()">
        📤 Publish
      </button>
    </div>
    
    <div class="preview-container">
      <div class="preview-split-view">
        <!-- Left: Markdown Source -->
        <div class="preview-source">
          <h3>📝 Markdown Source</h3>
          <textarea id="preview-markdown" rows="30"></textarea>
        </div>
        
        <!-- Right: Portal Preview -->
        <div class="preview-render">
          <h3>🖼️ Portal View</h3>
          <iframe id="preview-iframe" sandbox="allow-same-origin"></iframe>
        </div>
      </div>
    </div>
    
    <div class="preview-footer">
      <div class="preview-info">
        💡 Tip: Edit markdown on the left to see live updates on the right!
      </div>
    </div>
  </div>
</div>
```

### JavaScript Implementation
```javascript
// Portal Preview System
class PortalPreview {
  constructor() {
    this.iframe = null;
    this.markdownEditor = null;
    this.currentMode = 'desktop';
    this.autoRefresh = true;
  }
  
  open(customerName, markdownContent) {
    document.getElementById('portal-preview-modal').style.display = 'block';
    document.getElementById('preview-customer-name').textContent = customerName;
    
    this.markdownEditor = document.getElementById('preview-markdown');
    this.markdownEditor.value = markdownContent;
    
    this.iframe = document.getElementById('preview-iframe');
    
    // Setup live preview
    this.markdownEditor.addEventListener('input', () => {
      if (this.autoRefresh) {
        this.refresh();
      }
    });
    
    this.refresh();
  }
  
  refresh() {
    const markdown = this.markdownEditor.value;
    const html = this.renderMarkdownToPortal(markdown);
    
    // Inject into iframe with Portal CSS
    const iframeDoc = this.iframe.contentDocument || this.iframe.contentWindow.document;
    iframeDoc.open();
    iframeDoc.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portal Preview</title>
        <link rel="stylesheet" href="themes/portal.css">
        <style>
          body {
            margin: 0;
            padding: 0;
            font-family: 'Red Hat Text', sans-serif;
          }
          ${this.getPortalCSS()}
        </style>
      </head>
      <body>
        <div class="portal-preview">
          <div class="portal-header">
            <img src="public/redhat-logo.svg" alt="Red Hat" height="30">
          </div>
          <div class="portal-content">
            ${html}
          </div>
          <div class="portal-footer">
            <p>Page Maintenance Notice: This RFE/Bug tracker is maintained by Ansible TAM</p>
          </div>
        </div>
      </body>
      </html>
    `);
    iframeDoc.close();
    
    // Apply responsive mode
    this.setPreviewMode(this.currentMode);
  }
  
  renderMarkdownToPortal(markdown) {
    // Convert markdown to HTML with Portal-specific styling
    // Use a markdown library like marked.js or similar
    
    // For now, basic implementation
    let html = markdown
      // Headers
      .replace(/^# (.+)$/gm, '<h1>$1</h1>')
      .replace(/^## (.+)$/gm, '<h2>$1</h2>')
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      
      // Bold
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      
      // Links - JIRA
      .replace(/\[AAPRFE-(\d+)\]/g, '<a href="https://issues.redhat.com/browse/AAPRFE-$1" target="_blank">AAPRFE-$1</a>')
      .replace(/\[AAP-(\d+)\]/g, '<a href="https://issues.redhat.com/browse/AAP-$1" target="_blank">AAP-$1</a>')
      
      // Links - Support Cases
      .replace(/\[(\d{8})\]/g, '<a href="https://access.redhat.com/support/cases/#/case/$1" target="_blank">$1</a>')
      
      // Tables (basic)
      .replace(/\|(.+)\|/g, (match, content) => {
        const cells = content.split('|').map(c => c.trim());
        return '<tr>' + cells.map(c => `<td>${c}</td>`).join('') + '</tr>';
      })
      
      // Line breaks
      .replace(/\n/g, '<br>');
    
    return html;
  }
  
  getPortalCSS() {
    return `
      .portal-preview {
        max-width: ${this.currentMode === 'mobile' ? '375px' : '1200px'};
        margin: 0 auto;
        padding: 32px;
        background: white;
      }
      
      .portal-header {
        margin-bottom: 32px;
        padding-bottom: 16px;
        border-bottom: 2px solid #D2D2D2;
      }
      
      .portal-content {
        min-height: 500px;
      }
      
      .portal-footer {
        margin-top: 48px;
        padding-top: 16px;
        border-top: 1px solid #D2D2D2;
        color: #6A6E73;
        font-size: 14px;
      }
      
      h1 {
        font-size: 36px;
        font-weight: 700;
        color: #EE0000;
        margin-bottom: 24px;
      }
      
      h2 {
        font-size: 28px;
        font-weight: 600;
        color: #151515;
        margin-top: 32px;
        margin-bottom: 16px;
      }
      
      table {
        width: 100%;
        border-collapse: collapse;
        margin: 24px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      }
      
      th, td {
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid #F0F0F0;
      }
      
      th {
        background: #F5F5F5;
        font-weight: 600;
        border-bottom: 2px solid #D2D2D2;
      }
      
      tr:hover {
        background: #F9F9F9;
      }
      
      a {
        color: #0066CC;
        text-decoration: none;
        border-bottom: 1px solid transparent;
        transition: all 0.2s;
      }
      
      a:hover {
        border-bottom-color: #0066CC;
      }
    `;
  }
  
  setPreviewMode(mode) {
    this.currentMode = mode;
    this.refresh();
  }
  
  exportPreviewScreenshot() {
    // Use html2canvas or similar to capture iframe content
    console.log('Exporting screenshot...');
    // Implementation for screenshot export
  }
  
  close() {
    document.getElementById('portal-preview-modal').style.display = 'none';
  }
}

// Global instance
const portalPreview = new PortalPreview();

// Integration with report generation
function generateReport(customerName) {
  // ... generate markdown report
  const markdownReport = `
# ${customerName} RFE/Bug Tracker

**Summary**: 9 total cases (7 RFE, 2 Bug)

## Enhancement Requests (RFE)

| RED HAT JIRA ID | Support Case | Enhancement Request | Status |
|---|---|---|---|
| [AAPRFE-762] | [03666005] | [RFE] Add method for monitoring uwsgi workers | Backlog |
...
  `;
  
  // Open preview
  portalPreview.open(customerName, markdownReport);
}
```

## 🎯 Features

### Phase 1: Basic Preview (MVP)
- ✅ Split view (markdown + preview)
- ✅ Portal CSS emulation
- ✅ Live refresh
- ✅ Desktop view

### Phase 2: Enhanced
- 📱 Mobile/responsive preview
- 📸 Screenshot export
- 📤 Publish from preview
- 🔄 Auto-save drafts

### Phase 3: Advanced
- 🎨 Multiple portal themes
- 🔍 Zoom in/out
- 📊 Validation checks (broken links, etc.)
- 📏 Ruler/measurement tools
- 🎭 XP theme preview mode
- 📎 Clippy preview assistant

## 🚀 Integration Points

### With Clippy
```
📎 Clippy: "I see you're previewing a report! 
           Would you like me to check for:
           • Broken links
           • Spelling errors
           • Formatting issues
           • Missing information"
```

### With XP Theme
When XP theme is active, preview window uses XP styling but content still shows Portal view.

### With Report Generation
```javascript
// Update existing report flow
function showUpdate() {
  // ... existing code ...
  
  // Add preview button
  document.getElementById('content').innerHTML += `
    <button class="btn btn-secondary" onclick="previewReport()">
      🖼️ Preview in Portal
    </button>
  `;
}
```

## 📊 Success Metrics

1. **Error Reduction**: % decrease in report revisions
2. **Confidence**: TAM confidence in published reports
3. **Time Saved**: Minutes saved per report
4. **Adoption**: % of TAMs using preview before publish

---

**Status**: Designed, ready for implementation
**Effort**: 3-5 days
**Priority**: High (improves report quality)
**Dependencies**: Markdown parser, Portal CSS
**Integration**: Works with Clippy, XP theme, report generation

