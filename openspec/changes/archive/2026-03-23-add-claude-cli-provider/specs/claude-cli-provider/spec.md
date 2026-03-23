## ADDED Requirements

### Requirement: Claude CLI availability check

The Claude CLI provider SHALL verify that the `claude` command is available on the system PATH before attempting to generate commit messages.
The system SHALL exit with a clear error message and installation guidance when the CLI is not found.

#### Scenario: Claude CLI is installed

- **WHEN** the Claude CLI provider is selected and `claude --version` succeeds
- **THEN** the provider proceeds to generate commit messages

#### Scenario: Claude CLI is not installed

- **WHEN** the Claude CLI provider is selected and `claude` command is not found
- **THEN** the system exits with an error message indicating Claude CLI is not installed and provides installation guidance

### Requirement: Commit message generation via subprocess

The Claude CLI provider SHALL invoke `claude -p` with `--output-format json` and `--json-schema` flags to generate structured commit messages.
The prompt MUST include the git diff content and request exactly 5 conventional commit messages.

#### Scenario: Successful generation

- **WHEN** `claude -p` is invoked with a valid diff and JSON schema
- **THEN** the subprocess returns a JSON response containing exactly 5 commit message objects

#### Scenario: Claude CLI returns non-zero exit code

- **WHEN** `claude -p` exits with a non-zero return code
- **THEN** the system displays the stderr output and exits with an error

### Requirement: JSON schema for structured output

The Claude CLI provider SHALL pass a JSON schema via `--json-schema` that enforces the commit message output structure.
The schema SHALL require an object with a `messages` array of exactly 5 items, each containing `type`, `scope`, `description`, and `full_message` string fields.

#### Scenario: Schema enforces output structure

- **WHEN** the JSON schema is passed to `claude -p --json-schema`
- **THEN** the response conforms to the schema with exactly 5 commit message objects

### Requirement: Model selection with default

The Claude CLI provider SHALL pass the `--model` flag to `claude -p`.
The default model SHALL be `haiku` when no model is specified by the user.

#### Scenario: Default model

- **WHEN** no `--model` flag or `COMMIT_AI_MODEL` environment variable is set
- **THEN** the provider invokes `claude -p --model haiku`

#### Scenario: Custom model

- **WHEN** user specifies `--model sonnet`
- **THEN** the provider invokes `claude -p --model sonnet`

### Requirement: Local credential usage

The Claude CLI provider SHALL rely on the locally configured Claude CLI credentials.
The provider SHALL NOT require or read `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, or any other API token environment variables.

#### Scenario: Authenticated via CLI login

- **WHEN** user has authenticated Claude CLI locally (via `claude login` or subscription)
- **THEN** the provider generates commit messages without requiring additional token configuration

#### Scenario: CLI not authenticated

- **WHEN** the Claude CLI is installed but not authenticated
- **THEN** the `claude -p` subprocess fails and the system displays the error output from the CLI
