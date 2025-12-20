---
description: Security best practices for environment files and git
---

# Environment File Security

## Key Rules

1. **Never commit `.env` files with real secrets**

   - Add `.env` to `.gitignore` before first commit
   - Use `.env.example` with placeholder values only

2. **Standard .gitignore entries for env files**

```
# Environment files with secrets
.env
.env.local
.env.*.local
```

3. **If secrets were accidentally committed:**

   - Rotate the exposed API keys immediately
   - Remove from git tracking: `git rm --cached .env`
   - The secret is still in git history - consider using BFG Repo-Cleaner for full removal

4. **.env.example template (placeholders only)**

```
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Common .gitignore template

```
# Environment files
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
venv/
ENV/

# Database/State
*.db
*.json

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## Checking if secrets were pushed

```bash
git log --oneline --all -- ".env" ".env.example"
```

## Removing a file from git tracking (but keep locally)

```bash
git rm --cached <filename>
```
