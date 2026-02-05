# 🛠 IDE Setup Guide (Cursor / VS Code)

## Quick Start

If using **Dev Containers** (recommended):
1. Install "Dev Containers" extension
2. `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
3. All extensions and settings apply automatically

---

## Manual Setup

### Required Extensions

| Extension | ID | Purpose |
|-----------|-----|---------|
| Python | `ms-python.python` | Python language support |
| Pylance | `ms-python.vscode-pylance` | Type checking, IntelliSense |
| Ruff | `charliermarsh.ruff` | Fast linter + formatter |
| Docker | `ms-azuretools.vscode-docker` | Dockerfile, Compose support |
| GitLens | `eamodio.gitlens` | Git history, blame, annotations |
| Error Lens | `usernamehw.errorlens` | Inline error display |

### Recommended Extensions

| Extension | ID | Purpose |
|-----------|-----|---------|
| indent-rainbow | `oderwat.indent-rainbow` | Visualize indentation (crucial for Python) |
| YAML | `redhat.vscode-yaml` | YAML/docker-compose support |
| Even Better TOML | `tamasfe.even-better-toml` | pyproject.toml support |
| Material Icon Theme | `pkief.material-icon-theme` | Better file icons |
| Thunder Client | `rangav.vscode-thunder-client` | REST API testing |
| Jupyter | `ms-toolsai.jupyter` | Notebook support |

### Install via CLI

```bash
# Core
cursor --install-extension ms-python.python
cursor --install-extension ms-python.vscode-pylance
cursor --install-extension charliermarsh.ruff
cursor --install-extension ms-azuretools.vscode-docker
cursor --install-extension eamodio.gitlens
cursor --install-extension usernamehw.errorlens

# Recommended
cursor --install-extension oderwat.indent-rainbow
cursor --install-extension redhat.vscode-yaml
cursor --install-extension tamasfe.even-better-toml
cursor --install-extension pkief.material-icon-theme
cursor --install-extension rangav.vscode-thunder-client
cursor --install-extension ms-toolsai.jupyter
```

---

## Settings (settings.json)

Add to your user or workspace settings:

```json
{
  "editor.fontSize": 14,
  "editor.formatOnSave": true,
  "editor.minimap.enabled": false,
  "editor.rulers": [88, 120],
  "files.autoSave": "afterDelay",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "workbench.iconTheme": "material-icon-theme"
}
```

---

## Keyboard Shortcuts (Cursor-specific)

| Action | Shortcut | Notes |
|--------|----------|-------|
| AI Chat | `Ctrl+L` | Ask questions about code |
| AI Composer | `Ctrl+I` | Multi-file edits |
| Inline Edit | `Ctrl+K` | Edit selected code with AI |
| Command Palette | `Ctrl+Shift+P` | All commands |
| Go to File | `Ctrl+P` | Quick file open |
| Go to Symbol | `Ctrl+Shift+O` | Functions, classes in file |
| Find in Files | `Ctrl+Shift+F` | Search across project |
| Terminal | `Ctrl+\`` | Toggle terminal |
| Quick Fix | `Ctrl+.` | Code actions, fixes |
| Multi-cursor | `Alt+Click` | Add cursor |
| Select Next | `Ctrl+D` | Select next occurrence |

---

## Cursor-specific Features

### @ Mentions in Chat
- `@file.py` — reference specific file
- `@folder/` — reference folder
- `@Codebase` — search entire project
- `@Docs` — search library documentation
- `@web` — search internet

### Rules
Project-specific AI rules in `.cursorrules` file (already configured).

---

## Troubleshooting

**Pylance not finding imports?**
```bash
# Set Python interpreter
Ctrl+Shift+P → "Python: Select Interpreter" → choose .venv
```

**Ruff not formatting?**
```bash
# Check if ruff is installed
pip install ruff
```

**Extensions not installing?**
```bash
# Try VS Code CLI instead
code --install-extension <extension-id>
```
