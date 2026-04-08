from datetime import datetime, timedelta
from bson import ObjectId
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

TODAY = datetime(2025, 5, 1)


def days_from_today(n):
    return (TODAY + timedelta(days=n)).strftime("%Y-%m-%d")


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


class TestHomeworkUrgent:
    def _make_cursor(self, docs):
        mc = MagicMock()
        mc.to_list = AsyncMock(return_value=docs)
        return mc

    @pytest.mark.asyncio
    async def test_deadline_today_mark_today(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        hw = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "homework_name": "HW1",
            "deadline": "2025-05-01",
            "difficulty": "中等",
            "description": "",
            "status": "未完成",
            "score": 0,
            "image_id": None,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}

        with (
            patch("routers.homeworks.homeworks_col") as hw_col,
            patch("routers.homeworks.courses_col") as c_col,
            patch("routers.homeworks.datetime", FakeDatetime),
            patch("routers.homeworks.timedelta", timedelta),
        ):
            hw_col.find = MagicMock(return_value=self._make_cursor([hw]))
            hw_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)

            from routers.homeworks import urgent_homeworks

            result = await urgent_homeworks()

        assert len(result["items"]) == 1
        assert result["items"][0]["mark"] == "今天"
        assert result["items"][0]["days_left"] == 0

    @pytest.mark.asyncio
    async def test_deadline_day2_mark_urgent(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        hw = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "homework_name": "HW1",
            "deadline": "2025-05-03",
            "difficulty": "中等",
            "description": "",
            "status": "未完成",
            "score": 0,
            "image_id": None,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}

        with (
            patch("routers.homeworks.homeworks_col") as hw_col,
            patch("routers.homeworks.courses_col") as c_col,
            patch("routers.homeworks.datetime", FakeDatetime),
            patch("routers.homeworks.timedelta", timedelta),
        ):
            hw_col.find = MagicMock(return_value=self._make_cursor([hw]))
            hw_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)

            from routers.homeworks import urgent_homeworks

            result = await urgent_homeworks()

        assert len(result["items"]) == 1
        assert result["items"][0]["mark"] == "緊急"
        assert result["items"][0]["days_left"] == 2

    @pytest.mark.asyncio
    async def test_deadline_day3_mark_empty(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        hw = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "homework_name": "HW1",
            "deadline": "2025-05-04",
            "difficulty": "中等",
            "description": "",
            "status": "未完成",
            "score": 0,
            "image_id": None,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}

        with (
            patch("routers.homeworks.homeworks_col") as hw_col,
            patch("routers.homeworks.courses_col") as c_col,
            patch("routers.homeworks.datetime", FakeDatetime),
            patch("routers.homeworks.timedelta", timedelta),
        ):
            hw_col.find = MagicMock(return_value=self._make_cursor([hw]))
            hw_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)

            from routers.homeworks import urgent_homeworks

            result = await urgent_homeworks()

        assert len(result["items"]) == 1
        assert result["items"][0]["mark"] == ""
        assert result["items"][0]["days_left"] == 3

    @pytest.mark.asyncio
    async def test_deadline_day7_in_list(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        hw = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "homework_name": "HW1",
            "deadline": "2025-05-08",
            "difficulty": "中等",
            "description": "",
            "status": "未完成",
            "score": 0,
            "image_id": None,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}

        with (
            patch("routers.homeworks.homeworks_col") as hw_col,
            patch("routers.homeworks.courses_col") as c_col,
            patch("routers.homeworks.datetime", FakeDatetime),
            patch("routers.homeworks.timedelta", timedelta),
        ):
            hw_col.find = MagicMock(return_value=self._make_cursor([hw]))
            hw_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)

            from routers.homeworks import urgent_homeworks

            result = await urgent_homeworks()

        assert len(result["items"]) == 1
        assert result["items"][0]["days_left"] == 7

    @pytest.mark.asyncio
    async def test_deadline_day8_not_in_list(self):
        from datetime import datetime, timedelta

        TODAY = datetime(2025, 5, 1)

        class FakeDatetime:
            @staticmethod
            def now():
                return TODAY

            @staticmethod
            def strptime(s, fmt):
                return datetime.strptime(s, fmt)

        hw = {
            "_id": ObjectId(),
            "course_id": str(ObjectId()),
            "homework_name": "HW1",
            "deadline": "2025-05-09",
            "difficulty": "中等",
            "description": "",
            "status": "未完成",
            "score": 0,
            "image_id": None,
        }
        course = {"_id": ObjectId(), "course_name": "軟體工程"}

        with (
            patch("routers.homeworks.homeworks_col") as hw_col,
            patch("routers.homeworks.courses_col") as c_col,
            patch("routers.homeworks.datetime", FakeDatetime),
            patch("routers.homeworks.timedelta", timedelta),
        ):
            hw_col.find = MagicMock(return_value=self._make_cursor([hw]))
            hw_col.count_documents = AsyncMock(return_value=1)
            c_col.find_one = AsyncMock(return_value=course)

            from routers.homeworks import urgent_homeworks

            result = await urgent_homeworks()

        assert result["items"] == []


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
