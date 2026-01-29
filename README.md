# Git Auto-Commit with Gemini API

AI-powered git commit message generator using Gemini API's structured JSON output.

## What It Does

Analyzes your staged git changes and generates 5 Conventional Commits-compliant commit message suggestions using Gemini AI. Select one or enter your own.

## Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure API Key

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

For persistent configuration, add to your shell profile (~/.bashrc, ~/.zshrc):

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Configure Git Alias (Optional)

Add to your `~/.gitconfig`:

```ini
[alias]
    ac = !uv run --directory /your-script-path/git-auto-commit main.py
```

## Usage

### Basic Usage

```bash
git add <files>
uv run main.py
```

### With Git Alias

```bash
git add <files>
git ac
```

## Example

```
Analyzing staged changes...
Generating commit message options with Gemini API...

======================================================================
Select a commit message:
======================================================================
1. feat(auth): add user authentication system
2. feat: implement login and registration flow
3. chore(deps): add authentication dependencies
4. docs: update README with auth setup instructions
5. refactor(auth): restructure authentication module
6. Enter custom message
7. Cancel
======================================================================

Enter selection [1-7]:
```

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
