# 課程作業提醒系統

學期、課程、作業、考試的一站式管理平台

技術棧：FastAPI + React + MongoDB

---

## 開發者

國立中央大學 資訊工程學系 三年級

- 112403010 張詠蓁
- 112403555 陳柏安
- 112502539 蔡佳穎

---

## 專案結構

```
homework_system/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routers/
│   │   ├── semesters.py
│   │   ├── courses.py
│   │   ├── homeworks.py
│   │   └── exams.py
│   ├── test_homework_system.py
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── App.jsx
        ├── api/
        ├── components/
        └── pages/
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

## 啟動方式

### 1. Clone 專案

```bash
git clone https://github.com/zhen-0712/homework-system.git
cd homework-system
```

### 2. 啟動 MongoDB

```powershell
Get-Service -Name MongoDB
Start-Service -Name MongoDB
```

### 3. 後端

```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

後端啟動後：
- API：http://localhost:8000
- API 文件：http://localhost:8000/docs

### 4. 前端

```bash
cd frontend
npm install
npm run dev
```

前端啟動後：
- 網頁：http://localhost:5173

---

## 功能說明

| 頁面 | 功能 |
|------|------|
| 學期管理 | 新增、刪除學期，設定學年度與起訖日期 |
| 課程管理 | 依學期新增課程，記錄教師、時間、學分 |
| 新增作業 | 填寫作業名稱、截止日、難度、說明 |
| 作業查詢 | 依課程查詢作業，更新狀態與成績 |
| 本週待辦 | 顯示 7 天內截止的未完成作業 |
| 考試管理 | 新增考試，記錄時間、地點、範圍 |
| 考試提醒 | 顯示兩週內即將到來的考試 |

---

## API 端點

```
GET    /semesters/
POST   /semesters/
DELETE /semesters/{id}

GET    /courses/
POST   /courses/
DELETE /courses/{id}

GET    /homeworks/
GET    /homeworks/urgent
POST   /homeworks/
PATCH  /homeworks/{id}
DELETE /homeworks/{id}

GET    /exams/
GET    /exams/upcoming
POST   /exams/
PATCH  /exams/{id}
DELETE /exams/{id}
```

---

## 每日測試 log 執行方式

```powershell
cd D:\homework_system\backend
pytest test_homework_system.py -v --asyncio-mode=auto 2>&1 | Tee-Object test_log_YYYYMMDD.txt
git add test_log_YYYYMMDD.txt
git commit -m "test log dayN - YYYYMMDD"
git push
```

---

## 常見問題

**後端啟動失敗**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

**前端 CORS 錯誤**

確認 main.py 中 allow_origins 包含 http://localhost:5173，且後端正在執行。

**資料庫連線失敗**
```powershell
Get-Service -Name MongoDB
Start-Service -Name MongoDB
```