from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


# ── 學期 ────────────────────────────────────────────────────────
class SemesterCreate(BaseModel):
    year: str
    grade: str
    semester: str
    start_date: str
    end_date: str

class SemesterOut(SemesterCreate):
    id: str

# ── 課程 ────────────────────────────────────────────────────────
class CourseCreate(BaseModel):
    semester_id: str
    course_name: str
    teacher: str
    class_time: Optional[str] = ""
    credits: int = 3

class CourseOut(CourseCreate):
    id: str

# ── 作業 ────────────────────────────────────────────────────────
class HomeworkCreate(BaseModel):
    course_id: str
    homework_name: str
    deadline: str
    difficulty: str = "中等"
    description: Optional[str] = ""

class HomeworkUpdate(BaseModel):
    status: str
    score: int = 0

class HomeworkOut(HomeworkCreate):
    id: str
    status: str = "未完成"
    score: int = 0
    image_id: Optional[str] = None

# ── 考試 ────────────────────────────────────────────────────────
class ExamCreate(BaseModel):
    course_id: str
    semester_id: str | None = None
    exam_name: str
    exam_date: str
    exam_time: Optional[str] = ""
    location: Optional[str] = ""
    scope: Optional[str] = ""
    notes: Optional[str] = ""

class ExamUpdate(BaseModel):
    status: str
    score: int = 0

class ExamOut(ExamCreate):
    id: str
    status: str = "未考"
    score: int = 0
