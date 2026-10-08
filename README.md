# front-end-test

收集與整理我中意的視覺風格與 UI 元素，作為之後開發系統頁面時的設計參考庫。

## 用途

- **風格收藏**：記錄喜歡的整體視覺方向（配色、字體、版面、動態、質感）。
- **元素收藏**：保存可重用的介面元素範例（按鈕、卡片、導覽列、表單、表格、圖表區塊等）。
- **開發參考**：之後做系統頁面時，可以直接從這裡挑風格與元件，或交給 AI 依照這些參考產生頁面。

## 內建 Claude Code Skills

`.claude/skills/` 底下收錄了 [taste-skill](https://github.com/leonxlnx/taste-skill)（MIT）的一整套前端設計 skills，在 Claude Code 中以 `/安裝名稱` 呼叫，或直接用自然語言描述需求讓 Claude 自動套用。

| 類別 | Skill | 用途 |
| --- | --- | --- |
| 產生程式碼 | `design-taste-frontend` | 預設首選：判讀需求、調整 VARIANCE / MOTION / DENSITY 三個參數，產出不制式的頁面 |
| 產生程式碼 | `design-taste-frontend-v1` | 舊版 v1，僅在 v2 不合用時使用 |
| 產生程式碼 | `gpt-taste` | 更嚴格、版面變化更大、GSAP 動畫導向 |
| 產生程式碼 | `redesign-existing-projects` | 先盤點既有 UI 問題，再改善版面、間距與層級 |
| 產生程式碼 | `image-to-code` | 先產出設計圖、分析，再依圖實作 |
| 風格 | `high-end-visual-design` | 柔和、留白、高級感 |
| 風格 | `minimalist-ui` | Notion / Linear 式編輯風極簡 |
| 風格 | `industrial-brutalist-ui` | 工業粗獷風、瑞士字體排印 |
| 風格 | `stitch-design-taste` | Google Stitch 相容，可輸出 `DESIGN.md` |
| 輔助 | `full-output-enforcement` | 要求完整輸出，避免省略與佔位內容 |
| 只出圖 | `imagegen-frontend-web` | 網站設計稿圖片 |
| 只出圖 | `imagegen-frontend-mobile` | 手機 App 畫面圖片 |
| 只出圖 | `brandkit` | 品牌識別板圖片 |

使用範例：

```
/design-taste-frontend 做一個極簡、動畫少一點的後台登入頁
/minimalist-ui 把這個設定頁改成 Linear 風格
```

> 注意：`design-taste-frontend` 主要針對 landing page、作品集與改版；做資料密集的系統頁面（儀表板、表格）時，可搭配 `minimalist-ui` 或 `industrial-brutalist-ui`，並把 VISUAL_DENSITY 調高。

來源版本記錄於 `.claude/skills/TASTE-SKILL-SOURCE.txt`，授權見 `.claude/skills/TASTE-SKILL-LICENSE`。
