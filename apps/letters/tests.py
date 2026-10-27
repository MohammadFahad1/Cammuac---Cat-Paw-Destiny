from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Letter, LetterStatus

User = get_user_model()


class LetterAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="futureme@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.list_create_url = "/api/v1/letters/"

    def test_create_letter_initial_status_pending(self):
        payload = {
            "sticker": "bear",
            "title": "未來的我，你好！",
            "content": "希望那時候的我，已經實現了現在的夢想，不管遇到什麼困難，都不要放棄。"
        }
        response = self.client.post(self.list_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message_eng"], "Letter saved successfully.")
        self.assertEqual(response.data["message_chinese"], "信件保存成功。")

        data = response.data["data"]
        self.assertEqual(data["sticker"], "bear")
        self.assertEqual(data["title"], "未來的我，你好！")
        self.assertEqual(data["content"], payload["content"])
        self.assertEqual(data["status"], LetterStatus.PENDING)
        self.assertEqual(data["status_display"]["en"], "Pending")
        self.assertEqual(data["status_display"]["zh"], "待開啟")
        self.assertFalse(data["is_opened"])
        self.assertIsNone(data["opened_at"])
        self.assertIn("formatted_date_zh", data)
        self.assertIn("formatted_date_en", data)

        # Verify DB
        letter = Letter.objects.get(id=data["id"])
        self.assertEqual(letter.status, LetterStatus.PENDING)
        self.assertIsNone(letter.opened_at)

    def test_get_letter_detail_transitions_to_opened(self):
        letter = Letter.objects.create(
            user=self.user,
            sticker="cat",
            title="A message to open later",
            content="This letter is unopened initially.",
            status=LetterStatus.PENDING
        )
        detail_url = f"/api/v1/letters/{letter.id}/"

        # Initially pending in DB
        self.assertEqual(letter.status, LetterStatus.PENDING)
        self.assertIsNone(letter.opened_at)

        # View details -> must transition to opened!
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message_eng"], "Letter retrieved successfully.")
        self.assertEqual(response.data["message_chinese"], "成功获取信件详情。")

        data = response.data["data"]
        self.assertEqual(data["status"], LetterStatus.OPENED)
        self.assertEqual(data["status_display"]["en"], "Opened")
        self.assertEqual(data["status_display"]["zh"], "已開啟")
        self.assertTrue(data["is_opened"])
        self.assertIsNotNone(data["opened_at"])

        # Check DB updated
        letter.refresh_from_db()
        self.assertEqual(letter.status, LetterStatus.OPENED)
        self.assertIsNotNone(letter.opened_at)

    def test_get_already_opened_letter_preserves_timestamp(self):
        letter = Letter.objects.create(
            user=self.user,
            sticker="fish",
            title="Already opened",
            content="Testing already opened letter.",
            status=LetterStatus.PENDING
        )
        detail_url = f"/api/v1/letters/{letter.id}/"

        # Open first time
        res1 = self.client.get(detail_url)
        initial_opened_at = res1.data["data"]["opened_at"]
        self.assertIsNotNone(initial_opened_at)

        # Open second time -> status remains opened
        res2 = self.client.get(detail_url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["data"]["status"], LetterStatus.OPENED)

    def test_list_letters_with_status_filter(self):
        Letter.objects.create(user=self.user, sticker="1", content="Letter 1", status=LetterStatus.PENDING)
        Letter.objects.create(user=self.user, sticker="2", content="Letter 2", status=LetterStatus.PENDING)
        Letter.objects.create(user=self.user, sticker="3", content="Letter 3", status=LetterStatus.OPENED)

        # All letters
        res_all = self.client.get(self.list_create_url)
        self.assertEqual(res_all.status_code, status.HTTP_200_OK)
        self.assertEqual(res_all.data["total_count"], 3)
        self.assertEqual(res_all.data["pending_count"], 2)
        self.assertEqual(res_all.data["opened_count"], 1)
        self.assertEqual(len(res_all.data["data"]), 3)

        # Filter: pending
        res_pending = self.client.get(f"{self.list_create_url}?status=pending")
        self.assertEqual(len(res_pending.data["data"]), 2)
        for item in res_pending.data["data"]:
            self.assertEqual(item["status"], LetterStatus.PENDING)

        # Filter: opened
        res_opened = self.client.get(f"{self.list_create_url}?status=opened")
        self.assertEqual(len(res_opened.data["data"]), 1)
        self.assertEqual(res_opened.data["data"][0]["status"], LetterStatus.OPENED)

    def test_update_and_delete_letter(self):
        letter = Letter.objects.create(
            user=self.user,
            sticker="star",
            title="Old title",
            content="Old content",
            status=LetterStatus.PENDING
        )
        detail_url = f"/api/v1/letters/{letter.id}/"

        # Update
        update_res = self.client.put(detail_url, {
            "sticker": "leaf",
            "title": "New title",
            "content": "Updated content"
        }, format="json")
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(update_res.data["message_eng"], "Letter updated successfully.")
        self.assertEqual(update_res.data["message_chinese"], "信件更新成功。")
        self.assertEqual(update_res.data["data"]["title"], "New title")

        # Delete
        delete_res = self.client.delete(detail_url)
        self.assertEqual(delete_res.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_res.data["message_eng"], "Letter deleted successfully.")
        self.assertEqual(delete_res.data["message_chinese"], "信件已成功删除。")
        self.assertFalse(Letter.objects.filter(id=letter.id).exists())

    def test_patch_update_status_to_opened_and_pending(self):
        letter = Letter.objects.create(
            user=self.user,
            sticker="bear",
            title="Future Me",
            content="Testing patch status update",
            status=LetterStatus.PENDING
        )
        detail_url = f"/api/v1/letters/{letter.id}/"

        # Update status to opened via PATCH
        res_opened = self.client.patch(detail_url, {"status": "opened"}, format="json")
        self.assertEqual(res_opened.status_code, status.HTTP_200_OK)
        self.assertEqual(res_opened.data["data"]["status"], LetterStatus.OPENED)
        self.assertTrue(res_opened.data["data"]["is_opened"])
        self.assertIsNotNone(res_opened.data["data"]["opened_at"])

        letter.refresh_from_db()
        self.assertEqual(letter.status, LetterStatus.OPENED)
        self.assertIsNotNone(letter.opened_at)

        # Revert status to pending via PATCH
        res_pending = self.client.patch(detail_url, {"status": "pending"}, format="json")
        self.assertEqual(res_pending.status_code, status.HTTP_200_OK)
        self.assertEqual(res_pending.data["data"]["status"], LetterStatus.PENDING)
        self.assertFalse(res_pending.data["data"]["is_opened"])
        self.assertIsNone(res_pending.data["data"]["opened_at"])

        letter.refresh_from_db()
        self.assertEqual(letter.status, LetterStatus.PENDING)
        self.assertIsNone(letter.opened_at)

    def test_patch_invalid_status_rejected(self):
        letter = Letter.objects.create(
            user=self.user,
            content="Test letter",
            status=LetterStatus.PENDING
        )
        detail_url = f"/api/v1/letters/{letter.id}/"
        res = self.client.patch(detail_url, {"status": "archived"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(res.data["success"])

    def test_user_isolation(self):
        other_user = User.objects.create_user(
            email="otherletter@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        other_letter = Letter.objects.create(
            user=other_user,
            sticker="heart",
            title="Private Letter",
            content="Confidential future thoughts",
            status=LetterStatus.PENDING
        )

        # Should not appear in list
        list_res = self.client.get(self.list_create_url)
        self.assertEqual(list_res.data["total_count"], 0)

        # Detail GET should return 404
        detail_res = self.client.get(f"/api/v1/letters/{other_letter.id}/")
        self.assertEqual(detail_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(detail_res.data["message_eng"], "Letter not found.")
        self.assertEqual(detail_res.data["message_chinese"], "未找到该信件。")

        # PUT should return 404
        put_res = self.client.put(f"/api/v1/letters/{other_letter.id}/", {"content": "Hacked"}, format="json")
        self.assertEqual(put_res.status_code, status.HTTP_404_NOT_FOUND)

        # PATCH should return 404
        patch_res = self.client.patch(f"/api/v1/letters/{other_letter.id}/", {"status": "opened"}, format="json")
        self.assertEqual(patch_res.status_code, status.HTTP_404_NOT_FOUND)

        # DELETE should return 404
        delete_res = self.client.delete(f"/api/v1/letters/{other_letter.id}/")
        self.assertEqual(delete_res.status_code, status.HTTP_404_NOT_FOUND)

        # Status of other_user's letter must remain unchanged
        other_letter.refresh_from_db()
        self.assertEqual(other_letter.status, LetterStatus.PENDING)
        self.assertEqual(other_letter.content, "Confidential future thoughts")

    def test_unauthenticated_requests_rejected(self):
        self.client.credentials()  # Clear auth
        res_get = self.client.get(self.list_create_url)
        self.assertEqual(res_get.status_code, status.HTTP_401_UNAUTHORIZED)

        res_post = self.client.post(self.list_create_url, {"content": "Test"})
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)

