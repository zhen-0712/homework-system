from fastapi import APIRouter
from bson import ObjectId
from datetime import datetime, timedelta, date
from database import exams_col, courses_col, semesters_col
from models import ExamCreate, ExamUpdate, ExamOut
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/exams", tags=["exams"])


def _fmt(e) -> ExamOut:
    d = {
        k: (str(v) if isinstance(v, ObjectId) else v)
        for k, v in e.items()
        if k != "_id"
    }
    return ExamOut(id=str(e["_id"]), **d)


@router.get("/", response_model=list[ExamOut])
async def list_exams(course_id: str = None):
    q = {"course_id": course_id} if course_id else {}
    docs = await exams_col.find(q).sort("exam_date", 1).to_list(500)
    return [_fmt(d) for d in docs]


@router.get("/upcoming")
async def upcoming_exams():
    """未來兩週考試提醒"""
    today = datetime.now()
    two_weeks = today + timedelta(days=14)
    docs = await exams_col.find({"status": "未考"}).to_list(500)
    result = []
    for exam in docs:
        try:
            exam_date = datetime.strptime(exam["exam_date"], "%Y-%m-%d")
            if today <= exam_date <= two_weeks:
                days_left = (exam_date - today).days
                course = await courses_col.find_one(
                    {"_id": ObjectId(exam["course_id"])}
                )
                course_name = course["course_name"] if course else "未知課程"
                if days_left == 0:
                    mark = "今天"
                elif days_left <= 3:
                    mark = "緊急"
                elif days_left <= 7:
                    mark = "本週"
                else:
                    mark = ""
                result.append(
                    {
                        "id": str(exam["_id"]),
                        "exam_name": exam["exam_name"],
                        "course_name": course_name,
                        "exam_date": exam["exam_date"],
                        "exam_time": exam.get("exam_time", ""),
                        "location": exam.get("location", ""),
                        "days_left": days_left,
                        "mark": mark,
                    }
                )
        except Exception:
            continue
    result.sort(key=lambda x: x["days_left"])
    total = await exams_col.count_documents({"status": "未考"})
    return {"items": result, "total_upcoming": total}


@router.post("/", response_model=ExamOut)
async def create_exam(data: ExamCreate):
    try:
        input_date_dt = datetime.strptime(data.exam_date, "%Y-%m-%d")
        input_date = input_date_dt.date()
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )

    # 2. 檢查學期範圍 (確保 semesters_col 被用到)
    # 注意：這裡要用 data.semester_id
    semester = await semesters_col.find_one({"_id": ObjectId(data.semester_id)})
    if semester:
        start = datetime.strptime(semester["start_date"], "%Y-%m-%d")
        end = datetime.strptime(semester["end_date"], "%Y-%m-%d")
        
        if not (start <= input_date_dt <= end):
            raise HTTPException(
                status_code=400,
                detail=f"Exam date {data.exam_date} is outside the semester range"
            )
    # 3. 檢查是否為過去日期
    if input_date < date.today():
        raise HTTPException(
            status_code=400,
            detail=f"Cannot create an exam for a past date: {data.exam_date}",
        )

    payload = data.model_dump()
    payload["status"] = "未考"
    payload["score"] = 0
    result = await exams_col.insert_one(payload)
    doc = await exams_col.find_one({"_id": result.inserted_id})
    return _fmt(doc)

@router.patch("/{exam_id}", response_model=ExamOut)
async def update_exam(exam_id: str, data: ExamUpdate):
    await exams_col.update_one(
        {"_id": ObjectId(exam_id)},
        {"$set": {"status": data.status, "score": data.score}},
    )
    doc = await exams_col.find_one({"_id": ObjectId(exam_id)})
    return _fmt(doc)


@router.delete("/{exam_id}")
async def delete_exam(exam_id: str):
    await exams_col.delete_one({"_id": ObjectId(exam_id)})
    return {"ok": True}
