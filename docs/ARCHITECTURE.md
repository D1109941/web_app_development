# 系統架構設計文件 (ARCHITECTURE)

## 1. 技術架構說明

- **選用技術與原因**
  - **後端架構**：Python + Flask。原因為 Flask 輕量且彈性十足，非常適合此專案的 MVP 規模，能夠讓團隊快速開發出系統原型。
  - **模板引擎**：Jinja2。能與 Flask 無縫介接，在伺服器端將抓出的食譜資料動態塞入 HTML 中，適合不需複雜前後端分離（如 SPA）的專案，降低 API 設計上的開發成本。
  - **資料庫**：SQLite。免安裝與免伺服器設定的輕量級關聯式資料庫，非常適合用在本地端開發及初期運作。

- **Flask MVC 模式說明**
  - **Model（模型）**：負責定義資料庫的表格結構與商業邏輯（例如：「使用者」、「食譜」、「準備清單」等物件）。
  - **View（視圖）**：負責介面呈現。此架構中由 Jinja2 模板（`.html` 檔案）負責，它將接收 Controller 傳來的資料並渲染為瀏覽器看得懂的 HTML。
  - **Controller（控制器）**：由 Flask 的路由設計（Routings, 例如 `@app.route`）擔任，扮演橋樑角色。當瀏覽器發出請求時，Controller 請求 Model 取出對應資料，接著將資料交給 View 去產生結果。

## 2. 專案資料夾結構

```text
web_app_development/
├── app/                        ← 主要應用程式目錄
│   ├── __init__.py             ← 建立 Flask App、初始化擴充套件與載入路由
│   ├── models/                 ← 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── user.py             ← 使用者帳號模型
│   │   └── recipe.py           ← 食譜、食材清單與收藏模型
│   ├── routes/                 ← Flask 路由 (Controller)，以 Blueprint 切割
│   │   ├── __init__.py
│   │   ├── auth.py             ← 處理會員登入與註冊
│   │   ├── recipe.py           ← 處理食譜的瀏覽、搜尋及管理員新增刪除
│   │   └── collection.py       ← 處理儲存食譜與食材準備清單
│   ├── templates/              ← Jinja2 HTML 模板 (View)
│   │   ├── base.html           ← 包含共用導覽列及底部的基礎版型
│   │   ├── auth/               ← 登入 / 註冊相關頁面
│   │   ├── recipe/             ← 食譜搜尋列表 / 獨立食譜觀看頁面
│   │   └── collection/         ← 個人儲存總覽 / 食材準備清單頁面
│   └── static/                 ← 各種靜態檔案 (前端資源)
│       ├── css/style.css       ← 網頁樣式
│       ├── js/main.js          ← 前端互動邏輯 (例如：計時器功能實作)
│       └── images/             ← 網站素材或預設圖片
├── instance/                   ← 放置不會進入版控的環境依賴或私人檔案
│   └── database.db             ← SQLite 本機資料庫存放處
├── docs/                       ← 專案文件目錄
│   ├── PRD.md                  ← 產品需求文件
│   └── ARCHITECTURE.md         ← 系統架構設計文件
├── requirements.txt            ← 專案的 Python 套件依賴列表
├── config.py                   ← 專案系統設定 (例如 Secret Key, DB 位置)
└── run.py                      ← 系統主要進入點，用來啟動 Web Server
```

## 3. 元件關係圖

以下圖示表明當一個使用者向系統要資料時，內部元件的互動順序：

```mermaid
flowchart LR
    Browser[瀏覽器]
    Router[Flask Route\n(Controller)]
    Model[Model\n(Database Query)]
    DB[(SQLite DB)]
    Template[Jinja2 Template\n(View)]

    Browser <-- 1. HTTP 請求 /\n6. 回傳 HTML 畫面 --> Router
    Router <-- 2. 取用實體方法 /\n 4. 返回資料結果 --> Model
    Model <-- 3. SQL 查詢 / 寫入 --> DB
    Router -- 5. 將資料送交綁定 --> Template
    Template -. 渲染畫面 .-> Router
```

**元件關聯說明**：
1. **瀏覽器**發出請求，例如點擊「食譜詳細頁」。
2. `Flask Route` 收得請求後，透過 `Model` 去索取這份食譜的所有資料與成份。
3. `Model` 使用 SQL 語法與 `SQLite DB` 進行互動。
4. 取出資料後，傳遞回 Controller。
5. Controller 將食譜的 Python 資料送到 `Jinja2`，要求以 `recipe/detail.html` 的排版進行組裝。
6. 組裝完成後的 HTML，再透過 `Flask Route` 吐回給**瀏覽器**觀看。

## 4. 關鍵設計決策

1. **單體式伺服器渲染 (Server-Side Rendering)**
   - **說明**：專案採 Flask + Jinja2，而非使用前後端分離（如 React + API 操作）。
   - **原因**：為了減輕 API 防護與串接的複雜度，有助於讓 MVP 開發盡早且穩定地上線測試。

2. **路由採用 Flask Blueprint 切割模組**
   - **說明**：將路由切割為 `auth.py`, `recipe.py`, `collection.py` 三大塊。
   - **原因**：如果所有 `@app.route` 擠在 `app.py` 中將不利於後期的維護及分工。透過 Blueprint 能各自管理該模組的流程。

3. **登入狀態的控管機制 (Session)**
   - **說明**：使用 Flask 內建的 Secure Cookie Session 來記憶登入狀態與權限鑑別。
   - **原因**：對於初期的系統來說，無需外掛 Redis。內建 Session 經過密鑰加密不可竄改，已能滿足使用者與管理員的身分識別保護。

4. **計時功能的技術職責分配**
   - **說明**：將計時功能留給前端層（JavaScript）運作，不進資料庫。
   - **原因**：計時本身是瀏覽器上的暫時行為，不需要儲存為持久化資料；因此把此實作留至 `static/js/main.js` 中撰寫邏輯，避免造成後端的資源消耗。
