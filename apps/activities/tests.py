from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DailyCheckIn

User = get_user_model()


class DailyCheckInAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="catlover@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.today_url = "/api/v1/daily-check-in/today/"
        self.legacy_today_url = "/api/v1/activities/today/"
        self.choices_url = "/api/v1/daily-check-in/choices/"

    def test_get_today_check_in_when_no_record_exists(self):
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertFalse(response.data["has_record"])
        self.assertIsNone(response.data["data"])
        self.assertEqual(response.data["message_eng"], "No check-in record found for today.")
        self.assertEqual(response.data["message_chinese"], "今日尚未签到。")
        self.assertNotIn("available_choices", response.data)

    def test_post_complete_today_check_in_success(self):
        response = self.client.post(self.today_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertTrue(response.data["has_record"])
        self.assertEqual(response.data["message_eng"], "Daily check-in completed successfully.")
        self.assertEqual(response.data["message_chinese"], "每日签到成功。")
        self.assertNotIn("available_choices", response.data)

        data = response.data["data"]
        self.assertIsNotNone(data)
        self.assertIn("good_for", data)
        self.assertIn("avoid", data)
        self.assertIn("quote", data)
        self.assertIn("lucky_color", data)
        self.assertIn("lucky_number", data)
        self.assertIn("lucky_direction", data)

        # Check subfields matching Today's Cat card
        self.assertEqual(len(data["good_for"]["items_en"]), 3)
        self.assertEqual(len(data["good_for"]["items_zh"]), 3)
        self.assertEqual(len(data["avoid"]["items_en"]), 3)
        self.assertEqual(len(data["avoid"]["items_zh"]), 3)
        self.assertIn("en", data["quote"])
        self.assertIn("zh", data["quote"])
        self.assertIn("hex", data["lucky_color"])
        self.assertIn("code", data["lucky_direction"])

        # Check date formatting helpers
        self.assertIn("day", data)
        self.assertIn("month_year", data)
        self.assertIn("weekday_en", data)
        self.assertIn("weekday_zh", data)

        # Verify DB persistence
        record = DailyCheckIn.objects.filter(user=self.user, date=timezone.localdate()).first()
        self.assertIsNotNone(record)

    def test_post_duplicate_check_in_same_day_rejected(self):
        # First check-in succeeds
        res1 = self.client.post(self.today_url, {}, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Second check-in on same day should be rejected
        res2 = self.client.post(self.today_url, {}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(res2.data["success"])
        self.assertEqual(
            res2.data["message_eng"],
            "You have already checked in today. Check-in is allowed once a day."
        )
        self.assertEqual(
            res2.data["message_chinese"],
            "今日已完成签到，每天只能签到一次。"
        )
        self.assertTrue(res2.data["has_record"])
        self.assertIsNotNone(res2.data["data"])

    def test_get_today_check_in_when_record_exists(self):
        # Perform check-in
        self.client.post(self.today_url, {}, format="json")

        # Now GET should return has_record=True and the record
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["has_record"])
        self.assertIsNotNone(response.data["data"])
        self.assertEqual(response.data["message_eng"], "Today's check-in retrieved successfully.")
        self.assertEqual(response.data["message_chinese"], "成功获取今日签到记录。")

    def test_legacy_activities_url_route(self):
        # Verify /api/v1/activities/today/ routes correctly to the check-in view
        response = self.client.get(self.legacy_today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["has_record"])

    def test_get_choices_endpoint(self):
        response = self.client.get(self.choices_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        choices = response.data["data"]
        self.assertIn("good_for_choices", choices)
        self.assertIn("avoid_choices", choices)
        self.assertIn("quotes", choices)
        self.assertIn("lucky_colors", choices)
        self.assertIn("lucky_directions", choices)

    def test_unauthenticated_request_rejected(self):
        self.client.credentials()  # Clear auth
        res_get = self.client.get(self.today_url)
        self.assertEqual(res_get.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("en", res_get.data["message"])
        self.assertIn("zh", res_get.data["message"])

        res_post = self.client.post(self.today_url, {})
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("en", res_post.data["message"])
        self.assertIn("zh", res_post.data["message"])
