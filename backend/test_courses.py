from bson import ObjectId
from unittest.mock import AsyncMock, MagicMock, patch
import pytest


class TestCourse:
    @pytest.mark.asyncio
    async def test_create_course_success(self):
        doc = {
            "_id": ObjectId(),
            "semester_id": "sem01",
            "course_name": "軟體工程",
            "teacher": "王老師",
            "class_time": "",
            "credits": 3,
        }
        insert_result = MagicMock()
        insert_result.inserted_id = doc["_id"]

        with patch("routers.courses.courses_col") as col:
            col.find_one = AsyncMock(side_effect=[None, doc])
            col.insert_one = AsyncMock(return_value=insert_result)

            from routers.courses import create_course
            from models import CourseCreate

            data = CourseCreate(
                semester_id="sem01", course_name="軟體工程", teacher="王老師", credits=3
            )
            result = await create_course(data)

        assert result.course_name == "軟體工程"

    @pytest.mark.asyncio
    async def test_create_duplicate_course_returns_400(self):
        from fastapi import HTTPException

        existing_doc = {
            "_id": ObjectId(),
            "semester_id": "sem01",
            "course_name": "軟體工程",
            "teacher": "王老師",
            "class_time": "",
            "credits": 3,
        }

        with patch("routers.courses.courses_col") as col:
            col.find_one = AsyncMock(return_value=existing_doc)

            from routers.courses import create_course
            from models import CourseCreate

            data = CourseCreate(
                semester_id="sem01", course_name="軟體工程", teacher="王老師", credits=3
            )
            with pytest.raises(HTTPException) as exc:
                await create_course(data)

        assert exc.value.status_code == 400

    @pytest.mark.asyncio
    async def test_delete_course(self):
        with patch("routers.courses.courses_col") as col:
            col.delete_one = AsyncMock(return_value=MagicMock())

            from routers.courses import delete_course

            result = await delete_course(str(ObjectId()))

        assert result == {"ok": True}
        col.delete_one.assert_called_once()
