// Custom Theme Switcher Dropdown for Homer Dashboard

(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThemeSwitcher);
  } else {
    initThemeSwitcher();
  }

  function initThemeSwitcher() {
    // Wait for Vue to mount
    setTimeout(() => {
      createThemeSwitcher();
    }, 500);
  }

  function createThemeSwitcher() {
    // Find the navbar or header
    const navbar = document.querySelector('.first-line') || document.querySelector('nav') || document.querySelector('header');
    if (!navbar) {
      console.log('Navbar not found, retrying...');
      setTimeout(createThemeSwitcher, 500);
      return;
    }

    // Check if already exists
    if (document.querySelector('.theme-dropdown-container')) {
      return;
    }

    // Available themes
    const themes = [
      { id: 'default', name: 'Default' },
      { id: 'red-hat-enterprise', name: 'Red Hat Enterprise' },
      { id: 'ocean-blue', name: 'Ocean Blue' },
      { id: 'forest-green', name: 'Forest Green' },
      { id: 'purple-haze', name: 'Purple Haze' },
      { id: 'sunset-orange', name: 'Sunset Orange' },
      { id: 'slate-gray', name: 'Slate Gray' },
      { id: 'cyberpunk', name: 'Cyberpunk' },
      { id: 'amber-warmth', name: 'Amber Warmth' },
      { id: 'rose-pink', name: 'Rose Pink' },
      { id: 'midnight', name: 'Midnight' }
    ];

    // Get current theme
    const currentTheme = localStorage.getItem('homer-theme') || 'default';

    // Create dropdown container
    const container = document.createElement('div');
    container.className = 'theme-dropdown-container';

    // Create dropdown button
    const button = document.createElement('button');
    button.className = 'theme-dropdown-button';
    button.innerHTML = '<i class="fas fa-palette"></i><span>Theme</span><i class="fas fa-chevron-down"></i>';
    button.addEventListener('click', toggleDropdown);

    // Create dropdown content
    const dropdownContent = document.createElement('div');
    dropdownContent.className = 'theme-dropdown-content';

    // Add theme options
    themes.forEach(theme => {
      const option = document.createElement('div');
      option.className = 'theme-option';
      option.dataset.theme = theme.id;
      if (theme.id === currentTheme) {
        option.classList.add('active');
      }

      option.innerHTML = `
        <span class="theme-option-indicator"></span>
        <span>${theme.name}</span>
      `;

      option.addEventListener('click', () => {
        selectTheme(theme.id);
      });

      dropdownContent.appendChild(option);
    });

    // Assemble the dropdown
    container.appendChild(button);
    container.appendChild(dropdownContent);

    // Insert into navbar
    navbar.appendChild(container);

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!container.contains(e.target)) {
        dropdownContent.classList.remove('show');
      }
    });
  }

  function toggleDropdown(e) {
    e.stopPropagation();
    const dropdown = e.currentTarget.nextElementSibling;
    dropdown.classList.toggle('show');
  }

  function selectTheme(themeId) {
    // Store theme preference
    localStorage.setItem('homer-theme', themeId);

    // Update active state
    document.querySelectorAll('.theme-option').forEach(option => {
      option.classList.remove('active');
      if (option.dataset.theme === themeId) {
        option.classList.add('active');
      }
    });

    // Apply theme colors
    applyTheme(themeId);

    // Close dropdown
    document.querySelector('.theme-dropdown-content').classList.remove('show');
  }

  function applyTheme(themeId) {
    // Get the current mode (light/dark)
    const isDark = document.body.classList.contains('is-dark') || 
                   (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);

    // Theme color mappings
    const themeColors = {
      'default': {
        light: { primary: '#ee0033', secondary: '#0088ce', hover: '#cc0000', background: '#f5f5f5', card: '#ffffff', text: '#363636', link: '#0088ce' },
        dark: { primary: '#ee0033', secondary: '#0088ce', hover: '#ff3355', background: '#1a1a1a', card: '#2b2b2b', text: '#eaeaea', link: '#0088ce' }
      },
      'red-hat-enterprise': {
        light: { primary: '#ee0033', secondary: '#0088ce', hover: '#cc0000', background: '#f5f5f5', card: '#ffffff', text: '#363636', link: '#ee0033' },
        dark: { primary: '#ee0033', secondary: '#0088ce', hover: '#ff3355', background: '#1a1a1a', card: '#2b2b2b', text: '#eaeaea', link: '#ff3355' }
      },
      'ocean-blue': {
        light: { primary: '#0077be', secondary: '#00aaff', hover: '#005a8c', background: '#e8f4f8', card: '#ffffff', text: '#2c3e50', link: '#0077be' },
        dark: { primary: '#00aaff', secondary: '#0088cc', hover: '#00ccff', background: '#0a1929', card: '#1a2332', text: '#b0c4de', link: '#00aaff' }
      },
      'forest-green': {
        light: { primary: '#2d8659', secondary: '#3eb573', hover: '#226644', background: '#f0f8f4', card: '#ffffff', text: '#2c3e2f', link: '#2d8659' },
        dark: { primary: '#3eb573', secondary: '#4caf50', hover: '#5fd96e', background: '#0d1f12', card: '#1a2e1f', text: '#b8d4c2', link: '#3eb573' }
      },
      'purple-haze': {
        light: { primary: '#7c3aed', secondary: '#a78bfa', hover: '#6d28d9', background: '#f5f3ff', card: '#ffffff', text: '#3f3f46', link: '#7c3aed' },
        dark: { primary: '#a78bfa', secondary: '#8b5cf6', hover: '#c4b5fd', background: '#1a1625', card: '#2a2438', text: '#d8b4fe', link: '#a78bfa' }
      },
      'sunset-orange': {
        light: { primary: '#ea580c', secondary: '#fb923c', hover: '#c2410c', background: '#fff7ed', card: '#ffffff', text: '#431407', link: '#ea580c' },
        dark: { primary: '#fb923c', secondary: '#f97316', hover: '#fdba74', background: '#1f1108', card: '#2f1f14', text: '#fed7aa', link: '#fb923c' }
      },
      'slate-gray': {
        light: { primary: '#475569', secondary: '#64748b', hover: '#334155', background: '#f8fafc', card: '#ffffff', text: '#1e293b', link: '#475569' },
        dark: { primary: '#94a3b8', secondary: '#64748b', hover: '#cbd5e1', background: '#0f172a', card: '#1e293b', text: '#e2e8f0', link: '#94a3b8' }
      },
      'cyberpunk': {
        light: { primary: '#ff00ff', secondary: '#00ffff', hover: '#cc00cc', background: '#f5f0ff', card: '#ffffff', text: '#2d1b4e', link: '#ff00ff' },
        dark: { primary: '#ff00ff', secondary: '#00ffff', hover: '#ff66ff', background: '#0d0221', card: '#1a0b3a', text: '#e0b0ff', link: '#ff00ff' }
      },
      'amber-warmth': {
        light: { primary: '#d97706', secondary: '#fbbf24', hover: '#b45309', background: '#fffbeb', card: '#ffffff', text: '#451a03', link: '#d97706' },
        dark: { primary: '#fbbf24', secondary: '#f59e0b', hover: '#fcd34d', background: '#1f1508', card: '#2f2314', text: '#fef3c7', link: '#fbbf24' }
      },
      'rose-pink': {
        light: { primary: '#e11d48', secondary: '#fb7185', hover: '#be123c', background: '#fff1f2', card: '#ffffff', text: '#4c0519', link: '#e11d48' },
        dark: { primary: '#fb7185', secondary: '#f43f5e', hover: '#fda4af', background: '#1f0811', card: '#2f141d', text: '#fecdd3', link: '#fb7185' }
      },
      'midnight': {
        light: { primary: '#1e40af', secondary: '#3b82f6', hover: '#1e3a8a', background: '#eff6ff', card: '#ffffff', text: '#1e3a8a', link: '#1e40af' },
        dark: { primary: '#3b82f6', secondary: '#60a5fa', hover: '#93c5fd', background: '#030712', card: '#111827', text: '#dbeafe', link: '#3b82f6' }
      }
    };

    const colors = themeColors[themeId];
    if (!colors) return;

    const mode = isDark ? 'dark' : 'light';
    const themeColors = colors[mode];

    // Apply CSS variables
    const root = document.documentElement;
    root.style.setProperty('--highlight-primary', themeColors.primary);
    root.style.setProperty('--highlight-secondary', themeColors.secondary);
    root.style.setProperty('--highlight-hover', themeColors.hover);
    root.style.setProperty('--background', themeColors.background);
    root.style.setProperty('--card-background', themeColors.card);
    root.style.setProperty('--text', themeColors.text);
    root.style.setProperty('--link', themeColors.link);
    root.style.setProperty('--link-hover', themeColors.hover);
  }

  // Apply saved theme on load
  const savedTheme = localStorage.getItem('homer-theme');
  if (savedTheme) {
    setTimeout(() => applyTheme(savedTheme), 100);
  }
})();

