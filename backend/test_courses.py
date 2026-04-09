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

    @pytest.mark.asyncio
    async def test_list_courses_returns_sorted_list(self):
        docs = [
            {
                "_id": ObjectId(),
                "semester_id": "sem01",
                "course_name": "系統概論",
                "teacher": "林老師",
                "class_time": "",
                "credits": 3,
            },
            {
                "_id": ObjectId(),
                "semester_id": "sem01",
                "course_name": "軟體工程",
                "teacher": "王老師",
                "class_time": "",
                "credits": 3,
            },
        ]

        with patch("routers.courses.courses_col") as col:
            col.find = MagicMock(return_value=AsyncMock())
            col.find.return_value.sort = MagicMock(return_value=col.find.return_value)
            col.find.return_value.to_list = AsyncMock(return_value=docs)

            from routers.courses import list_courses

            result = await list_courses()

        assert [c.course_name for c in result] == ["系統概論", "軟體工程"]

    @pytest.mark.asyncio
    async def test_list_courses_with_semester_filter(self):
        docs = [
            {
                "_id": ObjectId(),
                "semester_id": "sem02",
                "course_name": "資料庫",
                "teacher": "陳老師",
                "class_time": "",
                "credits": 3,
            },
        ]

        with patch("routers.courses.courses_col") as col:
            col.find = MagicMock(return_value=col)
            col.sort = MagicMock(return_value=col)
            col.to_list = AsyncMock(return_value=docs)

            from routers.courses import list_courses

            result = await list_courses(semester_id="sem02")

        col.find.assert_called_once_with({"semester_id": "sem02"})
        assert len(result) == 1
        assert result[0].semester_id == "sem02"

    @pytest.mark.asyncio
    async def test_create_course_with_defaults(self):
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

            data = CourseCreate(semester_id="sem01", course_name="軟體工程", teacher="王老師")
            result = await create_course(data)

        assert result.class_time == ""
        assert result.credits == 3
