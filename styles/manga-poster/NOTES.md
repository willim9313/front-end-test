# Hollow Road（AKIRA 式漫畫海報致敬）

- **來源**：[Pinterest](https://www.pinterest.com/pin/1149473504922105452/)，插畫 DeadKatBarks
- **作者**：DeadKatBarks（Katlego，南非插畫家），圖右下角有簽名。原圖是《艾爾登法環》× AKIRA 海報式的同人插畫，圖上標題是「ELDEN RING」。作者帳號：[Instagram @deadkatbarks](https://www.instagram.com/deadkatbarks/)、[ArtStation](https://seven-on-kat-art.artstation.com/)、[INPRNT](https://www.inprnt.com/gallery/7onkat/)；這張圖的原始貼文還沒找到。
- **檔案**：`assets/reference-poster.jpg`（Pinterest 原圖，只留在本機、不進 git）
- **版權**：插畫屬原作者，只作為風格參考。

## 風格重點

- 從正上方俯視的人物插畫、一條中央細軸線把畫面分成左右兩半。
- Anton 黑色窄體大字，疊上紅色毛筆片假名（Yuji Boku）。
- 霧藍底、炭黑線條、骨白、只在最痛的地方用紅。
- 元件都是直角；有深色版。

## 調性頁（`index.html`）

- **公開版不放插圖**：之前從零重畫的版本（`src/gen.py`）抓不到原作的味道，2026-10-31 決定拿掉。`assets/hero-figures.jpg`、`still-horse.jpg`、`still-knight.jpg` 現在是同尺寸的佔位圖（霧色底、虛線框、註明原作者），由 `src/placeholder.py` 產生（在 `src/` 執行 `uv run python placeholder.py`）。
- 本機的「原圖版」（`local-original/`，不進 git）是從原圖描成向量、換成頁面配色後的版本，只在自己電腦上看。
- 片名「Hollow Road」和所有文案都是虛構的。
