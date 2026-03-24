## 1. 修改 subprocess 呼叫方式（commit message generation via subprocess）

- [x] 1.1 加入 `--no-session-persistence` 旗標到 subprocess 呼叫
- [x] 1.2 改用 stdin 傳送 prompt（`input=prompt`），移除位置引數

## 2. 更新測試

- [x] 2.1 [P] 更新 `test_providers_claude_cli.py` 中驗證 subprocess 呼叫引數的測試，確認包含 `--no-session-persistence`
- [x] 2.2 [P] 更新測試驗證 prompt 透過 `input` 關鍵字引數傳入而非位置引數
