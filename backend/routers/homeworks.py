from fastapi import APIRouter, HTTPException, UploadFile, File
from bson import ObjectId
from datetime import datetime, timedelta
from database import homeworks_col, courses_col, semesters_col, images_col
from models import HomeworkCreate, HomeworkUpdate, HomeworkOut

router = APIRouter(prefix="/homeworks", tags=["homeworks"])

def _fmt(h) -> HomeworkOut:
    d = {k: (str(v) if isinstance(v, ObjectId) else v) for k, v in h.items() if k != "_id"}
    return HomeworkOut(id=str(h["_id"]), **d)


@router.get("/", response_model=list[HomeworkOut])
async def list_homeworks(course_id: str = None):
    q = {"course_id": course_id} if course_id else {}
    docs = await homeworks_col.find(q).sort("deadline", 1).to_list(1000)
    return [_fmt(d) for d in docs]


@router.get("/urgent")
async def urgent_homeworks():
    """本週待辦（7天內）"""
    today = datetime.now()
    week_end = today + timedelta(days=7)
    docs = await homeworks_col.find({"status": {"$ne": "已完成"}}).to_list(1000)
    result = []
    for hw in docs:
        try:
            deadline = datetime.strptime(hw["deadline"], "%Y-%m-%d")
            if today <= deadline <= week_end:
                days_left = (deadline - today).days
                course = await courses_col.find_one({"_id": ObjectId(hw["course_id"])})
                course_name = course["course_name"] if course else "未知課程"
                if days_left == 0:
                    mark = "今天"
                elif days_left <= 2:
                    mark = "緊急"
                else:
                    mark = ""
                result.append({
                    "id": str(hw["_id"]),
                    "homework_name": hw["homework_name"],
                    "course_name": course_name,
                    "deadline": hw["deadline"],
                    "days_left": days_left,
                    "mark": mark,
                    "status": hw["status"],
                    "difficulty": hw.get("difficulty", ""),
                })
        except Exception:
            continue
    result.sort(key=lambda x: x["days_left"])
    total = await homeworks_col.count_documents({"status": {"$ne": "已完成"}})
    return {"items": result, "total_incomplete": total}


@router.post("/", response_model=HomeworkOut)
async def create_homework(data: HomeworkCreate):
    payload = data.model_dump()
    payload["status"] = "未完成"
    payload["score"] = 0
    payload["image_id"] = None
    result = await homeworks_col.insert_one(payload)
    doc = await homeworks_col.find_one({"_id": result.inserted_id})
    return _fmt(doc)


@router.patch("/{hw_id}", response_model=HomeworkOut)
async def update_homework(hw_id: str, data: HomeworkUpdate):
    await homeworks_col.update_one(
        {"_id": ObjectId(hw_id)},
        {"$set": {"status": data.status, "score": data.score}}
    )
    doc = await homeworks_col.find_one({"_id": ObjectId(hw_id)})
    return _fmt(doc)


@router.post("/{hw_id}/image")
async def upload_image(hw_id: str, file: UploadFile = File(...)):
    content = await file.read()
    result = await images_col.insert_one({"data": content, "filename": file.filename})
    await homeworks_col.update_one(
        {"_id": ObjectId(hw_id)},
        {"$set": {"image_id": str(result.inserted_id)}}
    )
    return {"image_id": str(result.inserted_id)}


@router.delete("/{hw_id}")
async def delete_homework(hw_id: str):
    await homeworks_col.delete_one({"_id": ObjectId(hw_id)})
    return {"ok": True}
