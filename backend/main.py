from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import semesters, courses, homeworks, exams

app = FastAPI(title="課程作業提醒系統 API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(semesters.router)
app.include_router(courses.router)
app.include_router(homeworks.router)
app.include_router(exams.router)

@app.get("/")
async def root():
    return {"message": "課程作業提醒系統 API", "docs": "/docs"}
