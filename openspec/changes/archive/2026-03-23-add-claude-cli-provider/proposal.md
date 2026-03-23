## Why

目前 commit-with-ai 僅支援 Google Gemini API 作為 AI provider。為了讓 Claude 訂閱用戶（Pro/Max）能直接使用本地 Claude CLI 憑證產生 commit messages，需要新增 Claude CLI 作為第二個 provider。透過 `claude -p --json-schema` 的非互動模式呼叫，使用者無需額外設定 API key，實現零設定整合。

## What Changes

- 將單檔 `commit_with_ai.py` 重構為 Python package（`commit_with_ai/`）
- 新增 provider 抽象層，支援多 AI provider 切換
- 新增 Claude CLI provider，透過 subprocess 呼叫 `claude -p` 產生 commit messages
- 新增 `--provider` CLI flag 與 `COMMIT_AI_PROVIDER` 環境變數，用於選擇 provider（優先序：`--provider` > `COMMIT_AI_PROVIDER` > 預設 `gemini`）
- 新增 `--model` CLI flag 與對應環境變數，用於指定模型（Claude 預設 `haiku`）
- 保留現有 Gemini provider 功能不變

## Capabilities

### New Capabilities

- `provider-system`: Provider 抽象層與選擇機制，管理多 AI provider 的註冊、切換與設定
- `claude-cli-provider`: Claude CLI provider 實作，透過 `claude -p --json-schema` subprocess 呼叫產生 commit messages

### Modified Capabilities

（無）

## Impact

- 受影響程式碼：`commit_with_ai.py`（拆分為 package）、`pyproject.toml`（更新 build 設定與 entry point）
- 新增依賴：無（Claude CLI 為外部工具，不需 Python package 依賴）
- CLI 介面變更：新增 `--provider` 與 `--model` 參數
- 向後相容：既有 Gemini 使用者不受影響，預設行為不變
