## Why

claude-cli provider 透過 `subprocess.run()` 呼叫 `claude -p`，每次執行時 CLI 會將 session 資料寫入磁碟，對於單次非互動式呼叫完全不必要。此外，prompt（含完整 git diff）作為命令列引數傳入，大型 diff 可能觸及 shell 引數長度限制。

## What Changes

- 在 `claude -p` 呼叫中加入 `--no-session-persistence` 旗標，避免寫入 session 到磁碟
- 改用 stdin 傳送 prompt（透過 `subprocess.run(input=...)` ），取代命令列位置引數

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `claude-cli-provider`: subprocess 呼叫方式變更 — 新增 `--no-session-persistence` 旗標，prompt 改由 stdin 傳入

## Impact

- 受影響程式碼：`commit_with_ai/providers/claude_cli.py`
- 受影響測試：`tests/test_providers_claude_cli.py`
