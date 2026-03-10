# 📚 課程作業提醒系統

> 學期、課程、作業、考試的一站式管理平台
> 
> 技術棧：FastAPI + React + MongoDB

---

## 專案結構

```
homework_system/
├── backend/                  # FastAPI 後端
│   ├── main.py               # 入口 + CORS 設定
│   ├── database.py           # MongoDB 連線
│   ├── models.py             # Pydantic 資料模型
│   ├── routers/
│   │   ├── semesters.py      # 學期 CRUD
│   │   ├── courses.py        # 課程 CRUD
│   │   ├── homeworks.py      # 作業 CRUD + 本週待辦
│   │   └── exams.py          # 考試 CRUD + 考試提醒
│   └── requirements.txt
│
└── frontend/                 # React 前端（Vite）
    └── src/
        ├── App.jsx
        ├── api/              # API 呼叫封裝
        ├── components/       # 共用元件（Sidebar、Card、PageHeader）
        └── pages/            # 7 個功能頁面
```

---

## 環境需求

| 工具 | 版本 |
|------|------|
| Python | 3.12+ |
| Node.js | 18+ |
| MongoDB | 7.0+ |
| Git | 任意版本 |

---

## 本地端安裝與啟動

### 1. Clone 專案

```bash
git clone https://github.com/zhen-0712/homework-system.git
cd homework-system
```

---

### 2. 啟動 MongoDB

確認 MongoDB 服務正在執行（Windows）：

```powershell
# 確認服務狀態
Get-Service -Name MongoDB

# 若未啟動，手動啟動
Start-Service -Name MongoDB
```

MongoDB 預設跑在 `mongodb://localhost:27017`

---

### 3. 後端設定

```bash
cd backend

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境（Windows）
venv\Scripts\activate

# 安裝套件
pip install -r requirements.txt

# 啟動後端
uvicorn main:app --reload
```

後端啟動後：
- API 服務：http://localhost:8000
- 互動式文件：http://localhost:8000/docs

---

### 4. 前端設定

**開新的終端機視窗**，回到專案根目錄：

```bash
cd frontend

# 安裝套件
npm install

# 啟動前端
npm run dev
```

前端啟動後：
- 網頁介面：http://localhost:5173

---

### 5. 同時啟動（正常開發流程）

每次開發需要開兩個終端機：

**Terminal 1 — 後端**
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 — 前端**
```bash
cd frontend
npm run dev
```

打開瀏覽器進入 **http://localhost:5173** 開始使用。

---

## 功能說明

| 頁面 | 功能 |
|------|------|
| 學期管理 | 新增 / 刪除學期，設定學年度與起訖日期 |
| 課程管理 | 依學期新增課程，記錄教師、時間、學分 |
| 新增作業 | 填寫作業名稱、截止日、難度、說明 |
| 作業查詢 | 依課程查詢作業，更新狀態與成績 |
| 本週待辦 | 顯示 7 天內截止的未完成作業 |
| 考試管理 | 新增考試，記錄時間、地點、範圍 |
| 考試提醒 | 顯示兩週內即將到來的考試 |

---

## API 端點總覽

```
GET    /semesters/           取得所有學期
POST   /semesters/           新增學期
DELETE /semesters/{id}       刪除學期

GET    /courses/             取得課程（可依 semester_id 篩選）
POST   /courses/             新增課程
DELETE /courses/{id}         刪除課程

GET    /homeworks/           取得作業（可依 course_id 篩選）
GET    /homeworks/urgent     取得本週待辦作業
POST   /homeworks/           新增作業
PATCH  /homeworks/{id}       更新作業狀態與成績
DELETE /homeworks/{id}       刪除作業

GET    /exams/               取得考試（可依 course_id 篩選）
GET    /exams/upcoming       取得兩週內考試
POST   /exams/               新增考試
PATCH  /exams/{id}           更新考試狀態與成績
DELETE /exams/{id}           刪除考試
```

---

## 常見問題

**Q：後端啟動失敗，提示找不到 module**
```bash
# 確認虛擬環境已啟動
venv\Scripts\activate
pip install -r requirements.txt
```

**Q：前端出現 CORS 錯誤**

確認後端的 `main.py` 中 `allow_origins` 包含 `http://localhost:5173`，且後端正在執行。

**Q：資料庫連線失敗**

確認 MongoDB 服務正在執行：
```powershell
Get-Service -Name MongoDB
Start-Service -Name MongoDB
```

**Q：`node_modules` 資料夾不存在**
```bash
cd frontend
npm install
```

---

## 開發者

張詠蓁 — 國立中央大學 資訊工程學系 / 資訊管理學系