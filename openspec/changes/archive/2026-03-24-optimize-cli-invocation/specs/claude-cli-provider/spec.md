## MODIFIED Requirements

### Requirement: Commit message generation via subprocess

The Claude CLI provider SHALL invoke `claude -p` with `--no-session-persistence`, `--output-format json`, and `--json-schema` flags to generate structured commit messages.
The prompt SHALL be passed via stdin (standard input) instead of as a positional command-line argument.
The prompt MUST include the git diff content and request exactly 5 conventional commit messages.

#### Scenario: Successful generation

- **WHEN** `claude -p` is invoked with `--no-session-persistence`, a valid diff via stdin, and JSON schema
- **THEN** the subprocess returns a JSON response containing exactly 5 commit message objects

#### Scenario: Claude CLI returns non-zero exit code

- **WHEN** `claude -p` exits with a non-zero return code
- **THEN** the system displays the stderr output and exits with an error
