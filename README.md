# NewsLeopard API — AI Agent Skill

**讓 AI 助手直接操作 NewsLeopard 電子報與簡訊 API，涵蓋 EDM 行銷活動與 SureNotify 交易通知。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill Format](https://img.shields.io/badge/Format-Agent%20Skill-blue.svg)](https://agentskills.io)

---

## 關於電子豹

[電子豹（NewsLeopard）](https://newsleopard.com)是台灣企業首選的電子報行銷平台，超過 15,000 家企業採用。平台提供 Email EDM 行銷與 SMS 簡訊寄送服務，核心特色包括智慧會員名單管理、自動分析會員行為、以及雲端高效率寄送架構——每分鐘可發送 10,000 封郵件，到達率高達 99%。

電子豹同時提供 **SureNotify** 交易通知服務，專為訂單確認、密碼重設、驗證碼等即時通知情境設計，確保重要訊息準時送達。

---

## 功能特色

- **EDM API 整合**（20 個端點）— 聯絡人管理、行銷活動建立/排程/A-B 測試、成效報表匯出、範本、自動化腳本、帳戶餘額查詢
- **SureNotify API 整合**（11 個端點）— 交易信件寄送、簡訊發送、Webhook 管理、事件追蹤、寄件網域驗證
- **除錯流程** — 常見錯誤碼對照表、逐步排查指南（活動未開信、信件未送達、簡訊未到達、Webhook 未觸發）
- **QA 測試清單** — EDM API 與 SureNotify API 各項功能完整驗收項目

---

## 什麼是 Agent Skill？

Agent Skill 是一種遵循 [agentskills.io 開放標準](https://agentskills.io)的知識套件，讓 AI 程式助手在需要時自動載入特定領域的 API 規格、最佳實務與除錯知識。

一個 Skill 可以跨工具使用，支援以下主流 AI 程式助手：

| AI 工具 | 支援狀態 |
|---------|---------|
| Claude Code | ✅ |
| GitHub Copilot (VS Code) | ✅ |
| Cursor | ✅ |
| Windsurf | ✅ |
| OpenAI Codex | ✅ |
| OpenClaw | ✅ |

---

## 安裝方式

### 前置需求（Prerequisites）

| 安裝方式 | 需求 |
|---------|------|
| 快速安裝（`npx skills add`） | [Node.js](https://nodejs.org/) 18 以上（含 `npx`） |
| 手動安裝（`git clone`） | [Git](https://git-scm.com/) |

#### 快速安裝（推薦）

使用 `npx skills add` 一鍵安裝到目前專案：

```bash
npx skills add https://github.com/Newsleopard/nlm-open-skills
```

#### 手動安裝

從 GitHub clone 本專案到對應的 Skills 目錄即可。

### Claude Code

**專案安裝**（僅限單一專案）：

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.claude/skills/newsleopard-api
```

**全域安裝**（所有專案皆可使用）：

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.claude/skills/newsleopard-api
```

### GitHub Copilot (VS Code)

**專案安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.github/skills/newsleopard-api
```

**全域安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.copilot/skills/newsleopard-api
```

> 也支援 `.agents/skills/` 目錄。

### Cursor

**專案安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.cursor/skills/newsleopard-api
```

**全域安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.cursor/skills/newsleopard-api
```

> 也支援 `.agents/skills/` 目錄與 GitHub Remote Rule 匯入。

### Windsurf

**專案安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.windsurf/skills/newsleopard-api
```

**全域安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.codeium/windsurf/skills/newsleopard-api
```

### OpenAI Codex

**專案安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.agents/skills/newsleopard-api
```

**全域安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.agents/skills/newsleopard-api
```

**系統級安裝：**

```bash
sudo git clone https://github.com/Newsleopard/nlm-open-skills.git /etc/codex/skills/newsleopard-api
```

> 支援 symlink，可透過符號連結指向共用位置。

### OpenClaw

**專案安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <workspace>/skills/newsleopard-api
```

**全域安裝：**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.openclaw/skills/newsleopard-api
```

> 載入優先順序：workspace > `~/.openclaw/skills` > bundled。
> 可透過 `skills.load.extraDirs` 設定額外搜尋路徑。
> 若日後上架 ClawHub，可執行 `clawhub install <skill-slug>` 安裝。

---

## Skill 內容結構

```
newsleopard-api/
├── SKILL.md                        # Skill 主文件：API 總覽、快速對照表、整合模式
└── references/
    ├── edm-api.md                  # EDM API 完整參考：端點、參數、請求/回應範例
    ├── surenotify-api.md           # SureNotify API 完整參考：Email、SMS、Webhook、網域驗證
    └── debugging-qa.md             # 除錯指南與 QA 測試清單
```

| 檔案 | 說明 |
|------|------|
| `SKILL.md` | Skill 進入點，包含兩套 API 的快速對照表、認證方式、速率限制、常見整合流程 |
| `references/edm-api.md` | EDM API 全部端點的詳細規格，包含聯絡人、活動、A/B 測試、報表、範本、自動化 |
| `references/surenotify-api.md` | SureNotify API 全部端點的詳細規格，包含寄信、簡訊、Webhook 簽章驗證、網域認證 |
| `references/debugging-qa.md` | 常見問題排查流程、錯誤碼對照、EDM 與 SureNotify 分別的 QA 驗收清單 |

---

## 涵蓋的 API 範圍

### EDM API（行銷活動）

| 分類 | 端點 |
|------|------|
| 聯絡人管理 | 建立群組、查詢群組、匯入聯絡人（檔案/文字）、查詢匯入狀態、移除聯絡人 |
| 活動管理 | 提交活動、單次上傳活動、A/B 測試活動、刪除活動、暫停活動、查詢活動狀態 |
| 報表 | 取得活動代碼、活動成效、匯出報表、取得下載連結 |
| 範本 | 列出範本、取得範本內容 |
| 自動化 | 觸發/停止自動化腳本 |
| 帳戶 | 查詢餘額 |

### SureNotify API（交易通知）

| 分類 | 端點 |
|------|------|
| Email | 寄送信件 |
| SMS | 寄送簡訊 |
| Email Webhook | 建立/更新、查詢、刪除 |
| SMS Webhook | 建立/更新、查詢、刪除 |
| 事件查詢 | Email 事件、SMS 事件 |
| 網域驗證 | 建立驗證紀錄、驗證 DNS、移除網域 |

---

## 搭配 MCP Server 使用

除了 Agent Skill，電子豹也提供 **MCP Server**，讓 AI 助手直接操作平台功能，不需要寫程式。

### Skill vs MCP Server 的差異

| | Agent Skill | MCP Server |
|---|---|---|
| **用途** | 給 AI 編程助手使用的 API 知識庫 | 讓 AI 直接操作平台功能 |
| **使用情境** | 開發者寫程式時，AI 助手參考 API 規格來生成程式碼 | 行銷人員或任何人透過 AI 對話直接管理電子報 |
| **需要寫程式嗎？** | 是，AI 幫你寫串接 API 的程式碼 | 否，AI 直接執行操作 |
| **支援工具** | Claude Code、Copilot、Cursor、Windsurf、Codex、OpenClaw | Claude.ai、Claude Desktop、ChatGPT、Cursor |

### MCP Server 設定

電子豹 MCP Server 提供兩種傳輸協定：

- **SSE**（推薦，相容性最佳）：`https://mcp.newsleopard.com/sse`
- **Streamable HTTP**：`https://mcp.newsleopard.com/mcp`

使用 **OAuth 2.1** 認證，首次連線時會引導登入授權。

**Claude Desktop 設定範例：**

```json
{
  "mcpServers": {
    "newsleopard": {
      "url": "https://mcp.newsleopard.com/sse"
    }
  }
}
```

**Cursor 設定範例：**

```json
{
  "mcpServers": {
    "newsleopard": {
      "url": "https://mcp.newsleopard.com/sse"
    }
  }
}
```

MCP Server 提供 27 個工具，涵蓋活動管理、報表分析、名單管理、範本操作、自動化控制等完整功能。

---

## 使用情境範例

安裝 Skill 後，你可以用自然語言對 AI 助手下達指令，例如：

**EDM 行銷活動：**
- 「幫我用 NewsLeopard API 建立一個行銷活動，對 VIP 群組寄送促銷信」
- 「查詢上週所有活動的開信率和點擊率」
- 「匯入這份 CSV 聯絡人到指定群組」
- 「建立一個 A/B 測試活動，測試兩個不同的主旨」
- 「查詢目前帳戶剩餘的寄送額度」
- 「匯出上個月活動的詳細報表」

**SureNotify 交易通知：**
- 「用 SureNotify 寄送一封訂單確認信給客戶」
- 「設定 Webhook 接收 Email 送達和開信事件」
- 「驗證 Webhook 簽章的程式碼要怎麼寫？」
- 「幫我完成寄件網域的 SPF/DKIM 驗證流程」
- 「用 SureNotify 發送簡訊驗證碼」

**除錯與排查：**
- 「活動已寄出但沒有開信紀錄，要怎麼排查？」
- 「SureNotify 寄信回傳 sender domain unverified 要怎麼解？」
- 「API 回傳 40012 錯誤碼是什麼意思？」

---

## 除錯與 QA

此 Skill 內建完整的除錯指引與 QA 清單（詳見 [`references/debugging-qa.md`](newsleopard-api/references/debugging-qa.md)）：

**除錯流程：**
- 活動已寄出但無開信/點擊
- SureNotify 信件未送達
- 簡訊未送達
- Webhook 未收到事件

**QA 驗收清單：**
- EDM API — 認證、聯絡人、活動、A/B 測試、報表、範本（30+ 測試項目）
- SureNotify API — Email、SMS、Webhook、網域驗證（25+ 測試項目）

---

## 相關連結

- [NewsLeopard EDM API 文件](https://newsleopard.com/api/v1/)
- [SureNotify API 文件](https://newsleopard.com/surenotify/api/v1/)
- [NewsLeopard MCP Server](https://mcp.newsleopard.com) — 讓 AI 直接操作電子豹平台
- [Agent Skills 開放標準](https://agentskills.io)
- [Claude Code Skills 文件](https://docs.anthropic.com/en/docs/claude-code/skills)
- [GitHub Copilot Skills 文件](https://docs.github.com/en/copilot/using-github-copilot/using-extensions-to-integrate-external-tools-with-copilot-chat)
- [Cursor Skills 文件](https://docs.cursor.com/context/skills)
- [Windsurf Skills 文件](https://docs.codeium.com/windsurf/skills)
- [OpenAI Codex Skills 文件](https://developers.openai.com/codex/skills/)
- [OpenClaw Skills 文件](https://docs.openclaw.ai/tools/skills)

---

## 授權條款

本專案採用 [MIT License](LICENSE) 授權。

---

Made with ❤️ by the NewsLeopard Team
