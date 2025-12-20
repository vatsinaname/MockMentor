---
description: Professional dark theme Streamlit UI template
---

# Professional Streamlit UI Template

Use this template when building Streamlit applications that need a clean, enterprise-grade dark theme.

## Key Design Principles

- No emojis - use text only
- Zinc color palette for dark mode
- Inter font for typography
- Minimal borders and subtle separations

## Color Palette (Zinc)

```css
--background: #09090b;
--surface: #18181b;
--border: #27272a;
--text-primary: #fafafa;
--text-secondary: #a1a1aa;
--text-muted: #71717a;
--text-dim: #52525b;
--accent-blue: #3b82f6;
--status-red: #ef4444;
--status-yellow: #f59e0b;
--status-green: #22c55e;
```

## CSS Template

```css
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap");

* {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
  background: #09090b;
}

#MainMenu,
footer,
header {
  visibility: hidden;
}

section[data-testid="stSidebar"] {
  background: #09090b;
  border-right: 1px solid #27272a;
}

h1,
h2,
h3 {
  color: #fafafa !important;
  font-weight: 500 !important;
  background: none !important;
  -webkit-text-fill-color: #fafafa !important;
}

p,
span,
div {
  color: #a1a1aa;
}

.stChatMessage {
  background: transparent !important;
  border: none !important;
}

[data-testid="stChatMessage"] {
  padding: 16px 0;
  border-bottom: 1px solid #18181b;
}

.stChatInput > div {
  background: #18181b !important;
  border: 1px solid #27272a !important;
  border-radius: 6px;
}

div[data-testid="metric-container"] {
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 6px;
  padding: 16px;
}

.stButton > button {
  background: #18181b;
  color: #a1a1aa;
  border: 1px solid #27272a;
  border-radius: 6px;
}

.stButton > button:hover {
  background: #27272a;
  color: #fafafa;
}
```

## Component Patterns

### Section Header

```html
<p
  style="color: #52525b; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;"
>
  Section Title
</p>
```

### Stat Card

```html
<div
  style="background: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 16px;"
>
  <p style="color: #71717a; font-size: 11px; text-transform: uppercase;">
    Label
  </p>
  <p style="color: #fafafa; font-size: 24px; font-weight: 500;">Value</p>
</div>
```

### Topic Row with Status

```html
<div
  style="display: flex; justify-content: space-between; padding: 10px 12px; background: #18181b; border: 1px solid #27272a; border-radius: 6px;"
>
  <span style="color: #fafafa; font-size: 13px;">Topic Name</span>
  <span style="color: #22c55e; font-size: 12px;">80%</span>
</div>
```

## Usage Notes

- Always hide Streamlit branding (#MainMenu, footer, header)
- Use 6px border-radius for cards and inputs
- Keep typography sizes: 11px labels, 13px body, 18px brand, 24px metrics
- Text hierarchy: #fafafa (primary) > #a1a1aa (secondary) > #71717a (muted) > #52525b (dim)
