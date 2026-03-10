from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import semesters_col
from models import SemesterCreate, SemesterOut

router = APIRouter(prefix="/semesters", tags=["semesters"])

def _fmt(s) -> SemesterOut:
    return SemesterOut(id=str(s["_id"]), **{k: v for k, v in s.items() if k != "_id"})


@router.get("/", response_model=list[SemesterOut])
async def list_semesters():
    docs = await semesters_col.find().sort([("year", -1), ("grade", 1), ("semester", 1)]).to_list(200)
    return [_fmt(d) for d in docs]


@router.post("/", response_model=SemesterOut)
async def create_semester(data: SemesterCreate):
    existing = await semesters_col.find_one(
        {"year": data.year, "grade": data.grade, "semester": data.semester}
    )
    if existing:
        raise HTTPException(status_code=400, detail="此學期已存在")
    result = await semesters_col.insert_one(data.model_dump())
    doc = await semesters_col.find_one({"_id": result.inserted_id})
    return _fmt(doc)


@router.delete("/{semester_id}")
async def delete_semester(semester_id: str):
    await semesters_col.delete_one({"_id": ObjectId(semester_id)})
    return {"ok": True}
