# 路由與頁面設計文件 (ROUTES)

本文件依據 PRD、ARCHITECTURE 與 DB_DESIGN 的規劃，定義 Flask 的路由 (Routes)、對應的 Jinja2 模板，以及預期執行的邏輯。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **會員管理 (Auth)** | | | | |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示會員註冊表單 |
| 註冊處理 | POST | `/auth/register` | — | 接收表單並建立帳號，重導向至登入頁 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示會員登入表單 |
| 登入處理 | POST | `/auth/login` | — | 驗證帳密，設定 Session，重導向至首頁 |
| 登出處理 | POST | `/auth/logout` | — | 清除 Session，重導向至登入頁或首頁 |
| **食譜瀏覽 (Recipe)** | | | | |
| 首頁/食譜列表 | GET | `/` | `templates/recipe/index.html` | 顯示食譜列表 (支援關鍵字或分類篩選) |
| 新增食譜頁面 | GET | `/recipe/new` | `templates/recipe/new.html` | 顯示新增食譜表單 (限管理員) |
| 新增食譜處理 | POST | `/recipe/new` | — | 寫入食譜與食材，重導向至首頁 |
| 食譜詳情 | GET | `/recipe/<id>` | `templates/recipe/detail.html` | 顯示單筆食譜圖文與成份，內含倒數計時器 |
| 編輯食譜頁面 | GET | `/recipe/<id>/edit` | `templates/recipe/edit.html` | 顯示編輯表單 (限管理員) |
| 編輯食譜處理 | POST | `/recipe/<id>/edit` | — | 更新食譜與食材紀錄 |
| 刪除食譜處理 | POST | `/recipe/<id>/delete`| — | 刪除食譜，重導向至首頁 (限管理員) |
| **收藏與清單 (Collection)**| | | | |
| 儲存/收藏食譜 | POST | `/collection/save/<id>`| — | 將食譜加入我的收藏紀錄 |
| 移除收藏 | POST | `/collection/remove/<id>`| — | 將食譜從清單移除 (取消收藏) |
| 我的收藏總覽 | GET | `/collection/` | `templates/collection/index.html` | 顯示個人已收藏的食譜 |
| 我的準備清單 | GET | `/collection/checklist`| `templates/collection/checklist.html`| 顯示儲存的食材清單，可點擊勾選 |
| 加入食材至清單| POST | `/collection/checklist/add` | — | 從食譜詳情頁一次加入部分或全部食材 |
| 切換準備狀態 | POST | `/collection/checklist/<id>/toggle`| — | 切換清單項目的勾選狀態 (API 存取) |

## 2. 每個路由的詳細說明

### Auth 模組 (auth.py)
* **`/auth/register` (GET/POST)**
  * **輸入**: POST 帶有 `username`, `password`, `confirm_password`。
  * **邏輯**: GET 渲染模板；POST 檢查密碼一致性後呼叫 `User.create()`，若 username 重複則回傳錯誤訊息並重新渲染。
  * **輸出**: 成功則 `redirect(url_for('auth.login'))`。
* **`/auth/login` (GET/POST)**
  * **輸入**: POST 帶有 `username`, `password`。
  * **邏輯**: 查詢 `User.get_by_username()` 比對 `password_hash`，成功則設定 `session['user_id'] = user['id']`。
  * **輸出**: 成功則 `redirect(url_for('recipe.index'))`，失敗重新渲染 `login.html`。
* **`/auth/logout` (POST)**
  * **邏輯**: 執行 `session.clear()` 登出。
  * **輸出**: `redirect(url_for('recipe.index'))`。

### Recipe 模組 (recipe.py)
* **`/` 此為網站入口 (GET)**
  * **輸入**: URL Query parameter `?q=keyword`。
  * **邏輯**: 呼叫 `Recipe.get_all(keyword)` 取出列表。
  * **輸出**: 渲染 `recipe/index.html`。
* **`/recipe/<id>` (GET)**
  * **邏輯**: 呼叫 `Recipe.get_by_id(id)` 與 `Ingredient.get_by_recipe(id)` 取出完整內容。
  * **輸出**: 渲染 `recipe/detail.html`。
* **`/recipe/new`, `/recipe/<id>/edit`, `/recipe/<id>/delete`**
  * **權限**: 限 `session['is_admin'] == 1` 的帳號操作，無權限則回傳錯誤或重導向。
  * **邏輯**: 操作對應的 `Recipe.*` 建立/更新方法，並透過 `Ingredient.clear_by_recipe()` 與 `Ingredient.add_to_recipe()` 重鑄食材。

### Collection 模組 (collection.py)
* **`/collection/save/<id>` (POST)**
  * **邏輯**: 確認有登入 (`user_id = session.get('user_id')`)，呼叫 `Collection.add(user_id, id)`。
  * **輸出**: 重導向回 `url_for('recipe.detail', id=id)`。
* **`/collection/` (GET)**
  * **邏輯**: 呼叫 `Collection.get_by_user(user_id)` 取得收藏列表。
  * **輸出**: 渲染 `collection/index.html`。
* **`/collection/checklist/add` (POST)**
  * **輸入**: 表單接收食材名稱與數量清單 (多筆，透過陣列命名欄位傳送)。
  * **邏輯**: 針對每一筆執行 `Checklist.add_item()` 存入使用者的準備庫裡。
  * **輸出**: 顯示推播訊息 (Flash)，回原來頁面或 `redirect(url_for('collection.checklist'))`。
* **`/collection/checklist` (GET)**
  * **邏輯**: 呼叫 `Checklist.get_by_user(user_id)` 讓前台檢視。
  * **輸出**: 渲染 `collection/checklist.html`。

## 3. Jinja2 模板清單

所有的 HTML 檔案皆放於 `app/templates/`。

* `base.html`：包含導覽列 (Navbar, 登入狀態切換)、底部聲明、CSS/JS 引入，所有子頁面皆繼承此模板 (`{% extends "base.html" %}`)。
* `auth/register.html`：會員註冊表單。
* `auth/login.html`：會員登入表單。
* `recipe/index.html`：首頁與搜尋結果，以漂亮或簡約的卡片列出食譜。
* `recipe/new.html`：新增/建立新食譜的總表單 (含動態增加/減少食材欄位的 UI)。
* `recipe/edit.html`：編輯舊有食譜的總表單。
* `recipe/detail.html`：單個食譜的檢視頁，包含內容、成分表、步驟圖文、前台專用倒數計時器及「加入收藏」按鈕交互。
* `collection/index.html`：個人的已收藏食譜列表歸檔。
* `collection/checklist.html`：採買與準備清單專頁，使用者可在這打勾「已買/未買」。

## 4. 路由骨架程式碼
系統已經根據這些設計建構了對應功能的 Flask Blueprint 檔案。位於專案下的 `app/routes/` 中。
