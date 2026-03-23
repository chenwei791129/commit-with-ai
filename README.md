# Commit with AI

AI-powered git commit message generator supporting multiple AI providers (Gemini API, Claude CLI).

## What It Does

Analyzes your staged git changes and generates 5 Conventional Commits-compliant commit message suggestions using AI. Select one or enter your own.

## Installation

### Via PyPI (Recommended)

```bash
# Use uvx (no installation required)
uvx commit-with-ai

# Or install globally
pip install commit-with-ai
```

### From Source

```bash
git clone https://github.com/chenwei791129/commit-with-ai.git
cd commit-with-ai
uv run -m commit_with_ai
```

## Setup

### Provider Selection

Choose your AI provider via `--provider` flag or `COMMIT_AI_PROVIDER` environment variable:

```bash
# Use Gemini (default)
commit-with-ai

# Use Claude CLI
commit-with-ai --provider claude-cli

# Or set via environment variable
export COMMIT_AI_PROVIDER="claude-cli"
```

**Priority**: `--provider` flag > `COMMIT_AI_PROVIDER` env > default (`gemini`)

### Model Selection

Override the default model via `--model` flag or `COMMIT_AI_MODEL` environment variable:

```bash
# Use a specific model
commit-with-ai --provider claude-cli --model sonnet

# Or set via environment variable
export COMMIT_AI_MODEL="sonnet"
```

**Priority**: `--model` flag > `COMMIT_AI_MODEL` env > provider default

### Gemini Provider (Default)

Set your Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

| Setting | Default |
|---------|---------|
| Model   | `gemini-3-flash-preview` |

### Claude CLI Provider

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated locally. No API key needed — uses your existing Claude CLI credentials.

```bash
# Install Claude Code (if not already installed)
npm install -g @anthropic-ai/claude-code

# Authenticate
claude login
```

| Setting | Default |
|---------|---------|
| Model   | `haiku` |

### Configure Git Alias

```bash
# If installed via pip
git config --global alias.ac '!commit-with-ai'

# Or if using uvx (no installation)
git config --global alias.ac '!uvx commit-with-ai'
```

## Usage

```bash
git add <files>
git ac

# Or with provider/model options
git add <files>
commit-with-ai --provider claude-cli --model sonnet
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COMMIT_AI_PROVIDER` | AI provider (`gemini`, `claude-cli`) | `gemini` |
| `COMMIT_AI_MODEL` | AI model name | Provider-specific |
| `GEMINI_API_KEY` | Gemini API key (for gemini provider) | — |
| `GOOGLE_API_KEY` | Alternative Gemini API key | — |

## Example

```
Analyzing staged changes...
Generating commit message options with claude-cli (haiku)...

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
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
