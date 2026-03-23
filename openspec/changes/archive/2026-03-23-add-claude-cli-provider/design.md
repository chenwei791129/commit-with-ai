## Context

目前 commit-with-ai 是一個單檔 Python 腳本（`commit_with_ai.py`），硬編碼使用 Google Gemini API 產生 commit messages。為了支援 Claude CLI 作為第二個 provider，需要重構為 package 架構並引入 provider 抽象層。

Claude CLI 提供 `claude -p` 非互動模式，支援 `--json-schema` 做 structured output，可透過 subprocess 呼叫。使用者只需本地已安裝並認證 Claude CLI，無需額外設定 API key。

## Goals / Non-Goals

**Goals:**

- 將單檔重構為 Python package，支援多 provider 架構
- 新增 Claude CLI provider，透過 subprocess 呼叫 `claude -p`
- 提供 `--provider` 與 `--model` CLI 參數及對應環境變數
- 保持既有 Gemini 功能完全不變

**Non-Goals:**

- 不實作 Anthropic SDK 直接 API 呼叫（`claude-api` 模式）
- 不支援 `CLAUDE_CODE_OAUTH_TOKEN` 或 `ANTHROPIC_API_KEY` 認證
- 不新增其他 AI provider（如 OpenAI）
- 不變更 commit message 的格式或數量（維持 5 則）

## Decisions

### Package 結構

將 `commit_with_ai.py` 拆分為以下結構：

```
commit_with_ai/
  __init__.py
  __main__.py        # entry point, CLI 參數解析
  core.py            # 共用邏輯（git 操作、選單、commit）
  providers/
    __init__.py
    base.py          # Provider 抽象基底類別
    gemini.py        # Gemini provider（從原檔遷移）
    claude_cli.py    # Claude CLI provider（新增）
```

**理由**：每個 provider 獨立一個模組，便於維護和未來擴充。`core.py` 集中 git 操作等共用邏輯，避免重複。

### Provider 選擇優先序

```
--provider CLI flag > COMMIT_AI_PROVIDER 環境變數 > 預設 "gemini"
```

**理由**：CLI flag 最明確，環境變數適合持久設定，預設 gemini 確保向後相容。

### Claude CLI 呼叫方式

使用 `subprocess.run()` 呼叫：

```bash
claude -p \
  --output-format json \
  --json-schema '<schema>' \
  --model <model> \
  "<prompt>"
```

**理由**：`--json-schema` 確保 structured output 與 Gemini 的 `response_schema` 等效；`--output-format json` 讓回應易於解析。

### Model 預設值與設定

| Provider | 預設 model | CLI flag | 環境變數 |
|----------|-----------|----------|---------|
| gemini | `gemini-3-flash-preview`（維持現狀） | `--model` | `COMMIT_AI_MODEL` |
| claude-cli | `haiku` | `--model` | `COMMIT_AI_MODEL` |

**理由**：Haiku 速度快、成本低，適合 commit message 這類簡短任務。`--model` 與 `COMMIT_AI_MODEL` 讓兩個 provider 共用同一參數。

### CLI 參數解析

使用 `argparse` 取代目前的無參數設計。

**理由**：需要 `--provider` 和 `--model` 參數，`argparse` 是 Python 標準庫，不需額外依賴。

## Risks / Trade-offs

- **Claude CLI 未安裝**：使用者選擇 claude-cli provider 但未安裝 Claude CLI 時，需要明確的錯誤訊息引導安裝。→ 在 provider 初始化時檢查 `claude --version`，失敗時顯示安裝指引。
- **Claude CLI 版本相容性**：`--json-schema` 是較新的 flag，舊版可能不支援。→ 檢查版本或捕獲錯誤，提示使用者更新。
- **Subprocess 效能**：啟動 subprocess 有額外開銷（約 1-2 秒）。→ 對於 commit message 產生場景可接受。
- **Package 重構風險**：拆分檔案可能引入 import 問題。→ 確保 `pyproject.toml` 的 build 設定正確更新。
