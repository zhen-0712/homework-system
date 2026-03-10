from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import courses_col, semesters_col
from models import CourseCreate, CourseOut

router = APIRouter(prefix="/courses", tags=["courses"])

def _fmt(c) -> CourseOut:
    return CourseOut(id=str(c["_id"]), **{k: (str(v) if isinstance(v, ObjectId) else v)
                                           for k, v in c.items() if k != "_id"})


@router.get("/", response_model=list[CourseOut])
async def list_courses(semester_id: str = None):
    q = {"semester_id": semester_id} if semester_id else {}
    docs = await courses_col.find(q).sort("course_name", 1).to_list(500)
    return [_fmt(d) for d in docs]


@router.post("/", response_model=CourseOut)
async def create_course(data: CourseCreate):
    existing = await courses_col.find_one(
        {"semester_id": data.semester_id, "course_name": data.course_name}
    )
    if existing:
        raise HTTPException(status_code=400, detail="此學期已有相同課名")
    payload = data.model_dump()
    result = await courses_col.insert_one(payload)
    doc = await courses_col.find_one({"_id": result.inserted_id})
    return _fmt(doc)


@router.delete("/{course_id}")
async def delete_course(course_id: str):
    await courses_col.delete_one({"_id": ObjectId(course_id)})
    return {"ok": True}
