from bson import ObjectId
from unittest.mock import AsyncMock, MagicMock, patch
import pytest


class TestExamUpcoming:
    def _make_cursor(self, docs):
        mc = MagicMock()
        mc.to_list = AsyncMock(return_value=docs)
        return mc

    @pytest.mark.asyncio
    async def test_exam_today_mark_today(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "exam_date": "2025-05-01",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}
        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.timedelta", timedelta),
        ):
            ex_col.find = MagicMock(return_value=self._make_cursor([exam]))
            ex_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)
            from routers.exams import upcoming_exams

            result = await upcoming_exams()
        assert result["items"][0]["mark"] == "今天"
        assert result["items"][0]["days_left"] == 0

    @pytest.mark.asyncio
    async def test_exam_day3_mark_urgent(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "exam_date": "2025-05-04",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}
        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.timedelta", timedelta),
        ):
            ex_col.find = MagicMock(return_value=self._make_cursor([exam]))
            ex_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)
            from routers.exams import upcoming_exams

            result = await upcoming_exams()
        assert result["items"][0]["mark"] == "緊急"
        assert result["items"][0]["days_left"] == 3

    @pytest.mark.asyncio
    async def test_exam_day4_mark_this_week(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "exam_date": "2025-05-05",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}
        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.timedelta", timedelta),
        ):
            ex_col.find = MagicMock(return_value=self._make_cursor([exam]))
            ex_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)
            from routers.exams import upcoming_exams

            result = await upcoming_exams()
        assert result["items"][0]["mark"] == "本週"
        assert result["items"][0]["days_left"] == 4

    @pytest.mark.asyncio
    async def test_exam_day7_mark_this_week(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "exam_date": "2025-05-08",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}
        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.timedelta", timedelta),
        ):
            ex_col.find = MagicMock(return_value=self._make_cursor([exam]))
            ex_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)
            from routers.exams import upcoming_exams

            result = await upcoming_exams()
        assert result["items"][0]["mark"] == "本週"
        assert result["items"][0]["days_left"] == 7

    @pytest.mark.asyncio
    async def test_exam_day8_mark_empty(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "exam_date": "2025-05-09",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}
        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.timedelta", timedelta),
        ):
            ex_col.find = MagicMock(return_value=self._make_cursor([exam]))
            ex_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)
            from routers.exams import upcoming_exams

            result = await upcoming_exams()
        assert result["items"][0]["mark"] == ""
        assert result["items"][0]["days_left"] == 8

    @pytest.mark.asyncio
    async def test_exam_day14_in_list(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "exam_date": "2025-05-15",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}
        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.timedelta", timedelta),
        ):
            ex_col.find = MagicMock(return_value=self._make_cursor([exam]))
            ex_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)
            from routers.exams import upcoming_exams

            result = await upcoming_exams()
        assert len(result["items"]) == 1
        assert result["items"][0]["days_left"] == 14

    @pytest.mark.asyncio
    async def test_exam_day15_not_in_list(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "exam_date": "2025-05-16",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}
        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.timedelta", timedelta),
        ):
            ex_col.find = MagicMock(return_value=self._make_cursor([exam]))
            ex_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)
            from routers.exams import upcoming_exams

            result = await upcoming_exams()
        assert result["items"] == []

    @pytest.mark.asyncio
    async def test_create_exam_with_past_date(self):
        from datetime import datetime, timedelta
        from fastapi import HTTPException

        TODAY = datetime(2025, 5, 1)
        FIXED_TODAY = TODAY.date()

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        class FakeDate:
            @staticmethod
            def today():
                return FIXED_TODAY

        exam = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "exam_name": "期中考",
            "semester_id": str(ObjectId()),
            "exam_date": "2025-04-01",
            "exam_time": "",
            "location": "",
            "scope": "",
            "notes": "",
            "status": "未考",
            "score": 0,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程實務"}

        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.courses_col") as c_col,
            patch("routers.exams.datetime", FakeDatetime),
            patch("routers.exams.date", FakeDate),
            patch("routers.exams.timedelta", timedelta),
        ):
            from routers.exams import create_exam
            from models import ExamCreate

            with pytest.raises(HTTPException) as exc:
                await create_exam(ExamCreate(**exam))

        assert exc.value.status_code == 400

    @pytest.mark.asyncio
    async def test_create_exam_outside_semester_range_returns_400(self):
        from fastapi import HTTPException
        from datetime import datetime

        sem_id = str(ObjectId())
        mock_semester = {
            "_id": ObjectId(sem_id),
            "year": "113",
            "grade": "大三",
            "semester": "下學期",
            "start_date": "2026-02-23",
            "end_date": "2026-06-20",
        }

        invalid_exam = {
            "course_id": str(ObjectId()),
            "semester_id": sem_id,
            "exam_name": "期首測驗",
            "exam_date": "2026-01-15",
        }

        with (
            patch("routers.exams.exams_col") as ex_col,
            patch("routers.exams.semesters_col") as sem_col,
            patch("routers.exams.courses_col") as c_col,
        ):
            sem_col.find_one = AsyncMock(return_value=mock_semester)
            c_col.find_one = AsyncMock(return_value={"course_name": "軟工"})

            from routers.exams import create_exam
            from models import ExamCreate

            with pytest.raises(HTTPException) as exc:
                await create_exam(ExamCreate(**invalid_exam))

        assert exc.value.status_code == 400
        assert "range" in exc.value.detail or "範圍" in exc.value.detail
