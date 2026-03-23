## 1. POC 驗證

- [x] 1.1 撰寫 POC 腳本驗證 `claude -p --json-schema` 的 structured output 可行性

## 2. Package 結構重構

- [x] 2.1 建立 `commit_with_ai/` package 目錄結構（`__init__.py`、`__main__.py`、`core.py`、`providers/`）
- [x] 2.2 將 `commit_with_ai.py` 的共用邏輯（git 操作、選單、commit）遷移至 `core.py`
- [x] 2.3 更新 `pyproject.toml` 的 build 設定與 entry point 以適配 package 結構
- [x] 2.4 刪除舊的 `commit_with_ai.py` 單檔

## 3. Provider 抽象層（Provider interface contract、Provider selection）

- [x] 3.1 實作 provider 抽象基底類別（`providers/base.py`），定義 Provider interface contract 的 `generate_commit_messages` 介面
- [x] [P] 3.2 實作 CLI 參數解析（`argparse`），支援 `--provider` 與 `--model` flag
- [x] [P] 3.3 實作 Provider 選擇優先序邏輯：`--provider` flag > `COMMIT_AI_PROVIDER` 環境變數 > 預設 `gemini`（Provider selection via CLI flag、Provider selection via environment variable、Default provider is gemini）
- [x] [P] 3.4 實作 Model 預設值與設定邏輯：`--model` flag > `COMMIT_AI_MODEL` 環境變數 > 各 provider 預設值（Model selection via CLI flag and environment variable）

## 4. Gemini Provider 遷移

- [x] 4.1 將現有 Gemini API 呼叫邏輯遷移至 `providers/gemini.py`，實作 provider 介面（Provider returns structured messages）

## 5. Claude CLI Provider 實作

- [x] [P] 5.1 實作 Claude CLI 可用性檢查（Claude CLI availability check）
- [x] 5.2 實作 Claude CLI 呼叫方式：`claude -p` subprocess 呼叫，含 `--output-format json`、`--json-schema` 與 `--model` flag（Commit message generation via subprocess、JSON schema for structured output、Model selection with default）
- [x] 5.3 實作 JSON 回應解析，將 Claude CLI 輸出轉換為標準 commit message 格式（Local credential usage）

## 6. 整合測試與驗收

- [x] 6.1 驗證 `--provider` 與 `COMMIT_AI_PROVIDER` 的優先序邏輯（Invalid provider specified、CLI flag overrides environment variable、No provider configuration）
- [x] 6.2 驗證 Claude CLI provider 的錯誤處理（Claude CLI is not installed、Claude CLI returns non-zero exit code、CLI not authenticated）
- [x] [P] 6.3 驗證 Gemini provider 功能未受影響（回歸測試）
- [x] [P] 6.4 驗證 Claude CLI provider 的完整流程（Claude CLI is installed、Successful generation、Default model、Custom model、Authenticated via CLI login）

## 7. 文件更新

- [x] [P] 7.1 更新 README.md：新增 Claude CLI provider 使用說明、`--provider` 與 `--model` 參數文件、環境變數設定說明
- [x] [P] 7.2 更新 pyproject.toml description 與 keywords 以反映多 provider 支援
