from bson import ObjectId
from unittest.mock import AsyncMock, MagicMock, patch
import pytest


class TestSemester:
    @pytest.mark.asyncio
    async def test_create_semester_success(self):
        doc = {
            "_id": ObjectId(),
            "year": "113",
            "grade": "大三",
            "semester": "上學期",
            "start_date": "2024-09-01",
            "end_date": "2025-01-31",
        }
        insert_result = MagicMock()
        insert_result.inserted_id = doc["_id"]

        with patch("routers.semesters.semesters_col") as col:
            col.find_one = AsyncMock(side_effect=[None, doc])
            col.insert_one = AsyncMock(return_value=insert_result)

            from routers.semesters import create_semester
            from models import SemesterCreate

            data = SemesterCreate(
                year="113",
                grade="大三",
                semester="上學期",
                start_date="2024-09-01",
                end_date="2025-01-31",
            )
            result = await create_semester(data)

        assert result.year == "113"
        assert result.semester == "上學期"

    @pytest.mark.asyncio
    async def test_create_semester_invalid_date_range_returns_400(self):
        from fastapi import HTTPException

        doc = {
            "_id": ObjectId(),
            "year": "112",
            "grade": "大二",
            "semester": "上學期",
            "start_date": "2025-09-01",
            "end_date": "2025-02-23",
        }
        insert_result = MagicMock()
        insert_result.inserted_id = doc["_id"]

        with patch("routers.semesters.semesters_col") as col:
            col.find_one = AsyncMock(return_value=doc)

            from routers.semesters import create_semester
            from models import SemesterCreate

            data = SemesterCreate(
                year="112",
                grade="大二",
                semester="上學期",
                start_date="2024-09-01",
                end_date="2025-02-23",
            )
            with pytest.raises(HTTPException) as exc:
                await create_semester(data)

        assert exc.value.status_code == 400

    @pytest.mark.asyncio
    async def test_create_duplicate_semester_returns_400(self):
        from fastapi import HTTPException

        existing_doc = {
            "_id": ObjectId(),
            "year": "113",
            "grade": "大三",
            "semester": "上學期",
            "start_date": "2024-09-01",
            "end_date": "2025-01-31",
        }

        with patch("routers.semesters.semesters_col") as col:
            col.find_one = AsyncMock(return_value=existing_doc)

            from routers.semesters import create_semester
            from models import SemesterCreate

            data = SemesterCreate(
                year="113",
                grade="大三",
                semester="上學期",
                start_date="2024-09-01",
                end_date="2025-01-31",
            )
            with pytest.raises(HTTPException) as exc:
                await create_semester(data)

        assert exc.value.status_code == 400

    @pytest.mark.asyncio
    async def test_delete_semester(self):
        with patch("routers.semesters.semesters_col") as col:
            col.delete_one = AsyncMock(return_value=MagicMock())

            from routers.semesters import delete_semester

            result = await delete_semester(str(ObjectId()))

        assert result == {"ok": True}
        col.delete_one.assert_called_once()
