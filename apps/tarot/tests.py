from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CatTarotDraw

User = get_user_model()


class CatTarotAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="tarotfan@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.today_url = "/api/v1/tarot/today/"
        self.root_url = "/api/v1/tarot/"
        self.cat_tarot_alias_url = "/api/v1/cat-tarot/today/"

    def test_get_today_tarot_when_no_record_exists(self):
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertFalse(response.data["has_record"])
        self.assertIsNone(response.data["data"])
        self.assertEqual(response.data["message_eng"], "No cat tarot record found for today.")
        self.assertEqual(response.data["message_chinese"], "今日尚未抽取猫咪塔罗。")

    def test_post_draw_tarot_success(self):
        payload = {"card_number": 2}
        response = self.client.post(self.today_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertTrue(response.data["has_record"])
        self.assertEqual(response.data["message_eng"], "Cat tarot drawn successfully.")
        self.assertEqual(response.data["message_chinese"], "猫咪塔罗抽取成功。")

        data = response.data["data"]
        self.assertEqual(data["card_number"], 2)
        self.assertEqual(data["date"], str(timezone.localdate()))
        self.assertIn("day", data)
        self.assertIn("month_year", data)
        self.assertIn("weekday_en", data)
        self.assertIn("weekday_zh", data)
        self.assertIn("category", data)
        self.assertIn("tag", data)
        self.assertIn("title", data)
        self.assertIn("content", data)
        self.assertIn("en", data["title"])
        self.assertIn("zh", data["title"])
        self.assertIn("en", data["content"])
        self.assertIn("zh", data["content"])

        # Check DB record
        self.assertTrue(
            CatTarotDraw.objects.filter(user=self.user, date=timezone.localdate(), card_number=2).exists()
        )

    def test_post_duplicate_draw_same_day_rejected(self):
        # First draw succeeds
        res1 = self.client.post(self.today_url, {"card_number": 1}, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Second draw on same day fails
        res2 = self.client.post(self.today_url, {"card_number": 3}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(res2.data["success"])
        self.assertEqual(
            res2.data["message_eng"],
            "You have already drawn a cat tarot card today. Tarot draw is allowed once a day."
        )
        self.assertEqual(
            res2.data["message_chinese"],
            "今日已抽取猫咪塔罗，每天只能抽取一次。"
        )
        self.assertTrue(res2.data["has_record"])
        self.assertIsNotNone(res2.data["data"])
        self.assertEqual(res2.data["data"]["card_number"], 1)

    def test_post_invalid_card_number_rejected(self):
        # Card number < 1
        res_zero = self.client.post(self.today_url, {"card_number": 0}, format="json")
        self.assertEqual(res_zero.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(res_zero.data["success"])

        # Card number > 3
        res_four = self.client.post(self.today_url, {"card_number": 4}, format="json")
        self.assertEqual(res_four.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(res_four.data["success"])

        # Missing card_number
        res_missing = self.client.post(self.today_url, {}, format="json")
        self.assertEqual(res_missing.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(res_missing.data["success"])

    def test_get_today_tarot_when_record_exists(self):
        self.client.post(self.today_url, {"card_number": 3}, format="json")

        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertTrue(response.data["has_record"])
        self.assertEqual(response.data["data"]["card_number"], 3)
        self.assertEqual(response.data["message_eng"], "Today's cat tarot retrieved successfully.")
        self.assertEqual(response.data["message_chinese"], "成功获取今日猫咪塔罗指引。")

    def test_user_isolation(self):
        other_user = User.objects.create_user(
            email="othertarot@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        CatTarotDraw.objects.create(
            user=other_user,
            date=timezone.localdate(),
            card_number=1,
            category_en="Today's Guidance",
            category_zh="今日指引",
            title_en="Other Title",
            title_zh="其他標題",
            content_en="Other Content",
            content_zh="其他內容"
        )

        # Authenticated as self.user - should NOT see other_user's draw
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["has_record"])
        self.assertIsNone(response.data["data"])

    def test_alias_routes(self):
        # Test root url /api/v1/tarot/
        res_root = self.client.get(self.root_url)
        self.assertEqual(res_root.status_code, status.HTTP_200_OK)

        # Test /api/v1/cat-tarot/today/
        res_alias = self.client.get(self.cat_tarot_alias_url)
        self.assertEqual(res_alias.status_code, status.HTTP_200_OK)

    def test_unauthenticated_requests_rejected(self):
        self.client.credentials()  # Clear auth
        res_get = self.client.get(self.today_url)
        self.assertEqual(res_get.status_code, status.HTTP_401_UNAUTHORIZED)

        res_post = self.client.post(self.today_url, {"card_number": 1})
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)
