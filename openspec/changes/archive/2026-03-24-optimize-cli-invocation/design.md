## Context

claude-cli provider 目前透過 `subprocess.run(["claude", "-p", ..., prompt])` 呼叫 Claude Code CLI。每次呼叫時 CLI 會將 session 資料寫入磁碟，對單次 `-p` 模式完全不必要。此外 prompt 作為命令列引數傳入，受 OS 引數長度限制。

## Goals / Non-Goals

**Goals:**

- 減少磁碟 I/O（透過 `--no-session-persistence` 避免寫入 session）
- 改善大型 diff 的穩定性（透過 stdin 傳送 prompt）

**Non-Goals:**

- 不變更生成邏輯（message 數量、prompt 內容、schema 格式）
- 不變更 provider 介面或選單行為
- 不引入新的外部依賴

## Decisions

### 加入 `--no-session-persistence` 旗標

避免將 session 資料寫入磁碟。commit message 生成是一次性操作，不需要 session 記錄。

### 改用 stdin 傳送 prompt

透過 `subprocess.run(input=prompt)` 將 prompt 從 stdin 傳入，取代作為最後一個位置引數。好處：
- 避免 OS 命令列引數長度限制（Linux `ARG_MAX` 通常為 ~2MB，macOS 為 ~256KB）
- 不需要 shell escaping

## Risks / Trade-offs

- [Risk] 未來 CLI 版本可能變更 `--no-session-persistence` 行為 → 這是官方支援的旗標，風險低。
