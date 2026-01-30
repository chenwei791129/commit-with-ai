# Git Auto-Commit with Gemini API

AI-powered git commit message generator using Gemini API's structured JSON output.

## What It Does

Analyzes your staged git changes and generates 5 Conventional Commits-compliant commit message suggestions using Gemini AI. Select one or enter your own.

## Installation

### Via PyPI (Recommended)

```bash
# Use uvx (no installation required)
uvx git-auto-commit

# Or install globally
pip install git-auto-commit
```

### From Source

```bash
# Clone the repository
git clone https://github.com/chenwei791129/git-auto-commit.git
cd git-auto-commit

# Run directly with uv
uv run git_auto_commit.py
```

## Setup

### 1. Configure API Key

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

For persistent configuration, add to your shell profile (~/.bashrc, ~/.zshrc):

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 2. Configure Git Alias (Optional)

Choose one of the following based on your installation method:

```bash
# If installed via pip
git config --global alias.ac '!git-auto-commit'

# Or if using uvx (no installation)
git config --global alias.ac '!uvx git-auto-commit'

# Or if running from source
git config --global alias.ac '!/your-script-path/git-auto-commit/git_auto_commit.py'
```

## Usage

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
