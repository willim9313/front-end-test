# 風格規格卡（Style Spec）

每個風格研究頁都長得不一樣，這是刻意的；但「拿來用的人一定要知道的事」應該每頁都一樣、放在同一個位置、用同一種格式。這份文件定義那張統一的規格卡，並記錄 2026-10-31 的 review 結果。

---

## 1. 九個欄位

順序就是查閱的順序：先判斷能不能用，再拿顏色和字，最後看細節。

| # | 欄位 | 回答的問題 | `catalog.js` 欄位 |
| --- | --- | --- | --- |
| 1 | **身分與授權** | 這是什麼？出處？插圖能不能直接拿去用？ | `name`、`zh`、`summary`、`source`、`status` |
| 2 | **適用場景** | 適合做哪種頁面？不適合什麼？ | `fit`、`avoid` |
| 3 | **色彩角色** | 每個顏色負責什麼、面積多大？ | `colors[]` |
| 4 | **可讀性對比** | 哪些顏色可以拿來排字？ | 不用填，由 `colors` 自動算 |
| 5 | **字體角色** | 標題、內文、標籤、CJK 各用什麼？ | `typeRoles[]` |
| 6 | **版面與構圖** | 主軸、網格、留白、動線？ | `layout[]` |
| 7 | **質感與線條** | 顆粒、網版、線寬、圓角？ | `texture[]` |
| 8 | **動態與互動** | 有哪些動態？減少動態時怎麼退？ | `motion[]`、`reducedMotion` |
| 9 | **Do / Don't** | 最容易用壞的地方？ | `do[]`、`dont[]` |

`window.SPEC_FIELDS` 列出必填欄位；目錄頁載入時會在 console 印出缺漏（`[spec] <slug> 缺：…`），規格卡頂端也會顯示「規格不完整」。

## 2. 怎麼看

- **目錄頁**：每張卡片右上角的「規格」。
- **風格頁**：右下角的「← 目錄 ／ 規格」。手機上往下捲時會收起，往上捲就回來。
- 規格卡是共用的 `overview/spec.js`，畫在 Shadow DOM 裡，跟風格頁自己的 CSS 互不影響；風格頁的設計完全沒動，只在 `</body>` 前多兩個 script。
- 在目錄頁打開時，會從該風格的 `styles.css` 借用 `@font-face`，字體樣本用的就是真的字型。

規格卡上可以：點色碼複製；「複製 CSS 變數」一次拿到整組 `--paper`、`--ink`、`--accent`…（同角色第二個起加編號）。

## 3. 欄位寫法

```js
{
  slug: "fugu-anatomy",
  name: "Fugu Anatomy",
  zh: "三色網版河豚解剖圖",
  summary: "一句話說完這個風格。",
  source: { by: "作者／設計者不明", url: "https://…" },
  status: "original",            // original | public-domain | derived

  fit:   ["產品功能說明／拆解圖", "教學、新手導覽"],
  avoid: ["嚴肅的金融或醫療內容", "長篇文章"],

  colors: [
    // 第一個 paper 是量對比的基準，放最前面
    { hex: "#fdfdfb", role: "paper",       name: "白紙",   use: "底色",              area: "主" },
    { hex: "#225a6e", role: "ink",         name: "深藍",   use: "魚身、輪廓",        area: "主" },
    { hex: "#e0685a", role: "accent",      name: "珊瑚紅", use: "標題、引線",        area: "輔" },
    { hex: "#b8483b", role: "accent-text", name: "珊瑚紅（文字用）", use: "紅色小字", area: "點綴" },
  ],

  typeRoles: [
    { role: "大標", family: "Oswald", weight: "600", note: "粗窄、全大寫" },
    { role: "標籤", family: "Zen Maru Gothic", weight: "700", sample: "フグの解剖学", note: "" },
  ],

  layout:  ["…", "…"],
  texture: ["…"],
  motion:  ["…"],
  reducedMotion: "減少動態時頁面實際的行為（照 CSS／JS 寫，不要猜）。",
  do:   ["…"],
  dont: ["…"],
}
```

- **role**：`paper`（底）、`ink`（主要墨色／文字）、`mute`（次要文字）、`accent`（強調）、`support`（插畫或背景用的輔助色）。結尾是 `-text` 的是為了排小字而調暗的版本，只出現在規格卡，不出現在目錄卡片的色條上。
- **area**：`主`（大面積）、`輔`（次要）、`點綴`（只在一兩處）。
- **sample**：字型如果是只含頁面用字的子集（檔名有 `subset`），樣本要從那一頁實際用到的文字裡挑，不然會掉回系統字型。沒有 sample 時：樣式名稱是拉丁字就用名稱，否則用 `Aa Bb Cc 0123`。
- 色碼請取自該頁 `styles.css` 的 `:root` token，不要從參考圖重新取色。

---

## 4. Review 結果（2026-10-31）

### 測試範圍

在 `claude/keen-mendel-a0jtx0` 上，用本機伺服器跑目錄頁與 13 個風格頁，桌面寬度與 375px 手機寬度、淺色與深色都測過。

| 項目 | 結果 |
| --- | --- |
| Console 錯誤 | 只有 yerko-hamlet 的 `reference-spread.jpg` 404（檔案被 .gitignore 排除，頁面已處理成隱藏「Original」按鈕，屬預期）和 favicon |
| 圖片／字體載入 | 全部正常 |
| 375px 橫向捲動 | 13 頁與目錄都沒有 |
| 目錄篩選 | 類型、手法交集、文字搜尋、色碼搜尋、URL hash 讀寫、清除，全部正確 |
| catalog.js 與頁面一致性 | 每個色碼與字體都確實出現在對應頁面 |
| 規格卡 | 13 筆資料欄位完整；Esc、✕、點背景都能關；複製色碼與 CSS 變數可用 |
| 規格列遮擋 | 桌面 13 頁都不遮任何控制項；手機首屏在 hebitsukai（色票）、manga-poster（Watch trailer）會壓到全寬元件的一角，往下捲就收起 |

### 問題與處理狀態

| # | 問題 | 狀態 |
| --- | --- | --- |
| 1 | 規格資訊散在 catalog 與 NOTES，格式不一，3 頁沒寫色碼、只有 1 頁有字體角色 | ✅ 統一進 `catalog.js`，用規格卡呈現 |
| 2 | 沒有「哪些顏色能排字」的資訊 | ✅ 規格卡自動算對比並分級 |
| 3 | 風格頁回不到目錄 | ✅ 每頁右下角有「← 目錄」 |
| 4 | torino-editorial 沒有 NOTES.md | ✅ 已補 |
| 5 | NOTES.md 的標題順序不一（yerko 先寫調性頁、manga-poster 沒有「可以拿到網頁上的手法」） | ⏳ 未處理；規格資訊已不靠 NOTES，屬於整理性質 |
| 6 | 只有 3 頁有深色版 | 不改；規格卡標示「有／無深色版」 |
| 7 | 手機版目錄的篩選列佔掉整個第一屏 | ⏳ 未處理，建議收成一個「篩選」按鈕 |
| 8 | manga-poster、torino 從 unpkg 載入 Phosphor icons，離線時圖示消失 | ⏳ 未處理，建議改成本機檔 |
| 9 | 縮圖要重截時規格列會入鏡 | ✅ `thumbs.js` 截圖前會隱藏規格列 |

### 色彩對比（前景色 vs 紙色）

規格卡上即時顯示；這裡是 review 當下的快照。不少頁面已經為小字準備了調暗的版本（例如 manga-poster 的 `#9e2f28`、fugu 的 `#b8483b`），規格卡會一起列出。

| 風格 | 文字可用（≥4.5） | 只能大字（3–4.5） | 只能當色塊（<3） |
| --- | --- | --- | --- |
| manga-poster | `#1c1c1e`、`#9e2f28`（紅字用） | `#bc3a32` 4.05 | `#6e8c94` 2.63 |
| fugu-anatomy | `#225a6e`、`#b8483b`（紅字用） | `#1898b2` 3.34、`#e0685a` 3.27 | |
| hebitsukai-alley | `#023d5c` | | `#f86c42` 2.78、`#fccc9a` 1.41、`#a8eae0` 1.29 |
| ojisan-museum | `#333333`、`#8e5a54`（標誌） | | `#ea908a` 2.05 |
| kutepov-hunt | `#2e2c27` | `#c05a3c` 3.53 | |
| red-umbrella | `#1b1b1b` | `#c8322a` 4.30 | |
| yerko-hamlet | `#141414`、`#4a4a4a`、`#7d6553` | | |
| moon-window | `#243a3a`、`#9e2f22` | | |
| symbiotic-body | `#262626`、`#a8443c` | | |
| torino-editorial | `#1048b8` | | |
| ascent／big-issue／killoffer | 單一墨色，都 ≥ 11 | | |
