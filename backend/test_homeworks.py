from bson import ObjectId
from unittest.mock import AsyncMock, MagicMock, patch
import pytest


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
