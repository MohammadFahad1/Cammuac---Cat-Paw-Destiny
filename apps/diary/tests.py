from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DiaryNote

User = get_user_model()


class DiaryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="diaryuser@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.list_create_url = "/api/v1/diary/"
        self.alias_url = "/api/v1/my-diary/"

    def test_create_diary_note_success(self):
        payload = {
            "icon": "happy_cat",
            "date": "2026-10-27",
            "note": "Had a wonderful morning walk with my cat today!"
        }
        response = self.client.post(self.list_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message_eng"], "Diary note created successfully.")
        self.assertEqual(response.data["message_chinese"], "日记创建成功。")

        data = response.data["data"]
        self.assertEqual(data["icon"], "happy_cat")
        self.assertEqual(data["date"], "2026-10-27")
        self.assertEqual(data["note"], "Had a wonderful morning walk with my cat today!")
        self.assertEqual(data["day"], 27)
        self.assertEqual(data["weekday_en"], "Tue")
        self.assertEqual(data["weekday_zh"], "星期二")

        # Verify DB record
        self.assertTrue(DiaryNote.objects.filter(id=data["id"], user=self.user).exists())

    def test_create_diary_note_validation_error(self):
        # Missing note
        payload = {"icon": "happy_cat", "date": "2026-10-27"}
        response = self.client.post(self.list_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("en", response.data["message"])
        self.assertIn("zh", response.data["message"])

    def test_list_diary_notes_no_pagination(self):
        # Create 3 notes
        DiaryNote.objects.create(user=self.user, icon="icon1", date="2026-10-25", note="Note 1")
        DiaryNote.objects.create(user=self.user, icon="icon2", date="2026-10-26", note="Note 2")
        DiaryNote.objects.create(user=self.user, icon="icon3", date="2026-10-27", note="Note 3")

        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message_eng"], "Diary notes retrieved successfully.")
        self.assertEqual(response.data["message_chinese"], "成功获取日记列表。")
        self.assertEqual(response.data["count"], 3)
        self.assertIsInstance(response.data["data"], list)
        self.assertEqual(len(response.data["data"]), 3)
        # Should be ordered descending by date
        self.assertEqual(response.data["data"][0]["note"], "Note 3")

    def test_list_notes_only_returns_own_notes(self):
        other_user = User.objects.create_user(
            email="otheruser@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        DiaryNote.objects.create(user=self.user, icon="mine", date="2026-10-27", note="My note")
        DiaryNote.objects.create(user=other_user, icon="other", date="2026-10-27", note="Other note")

        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["data"][0]["note"], "My note")

    def test_get_diary_note_detail_success(self):
        note = DiaryNote.objects.create(
            user=self.user,
            icon="detail_icon",
            date="2026-10-27",
            note="Specific note for testing details."
        )
        detail_url = f"/api/v1/diary/{note.id}/"
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message_eng"], "Diary note details retrieved successfully.")
        self.assertEqual(response.data["message_chinese"], "成功获取日记详情。")
        self.assertEqual(response.data["data"]["id"], note.id)
        self.assertEqual(response.data["data"]["note"], "Specific note for testing details.")

    def test_get_diary_note_detail_not_found_or_other_user(self):
        # Non-existent ID
        response = self.client.get("/api/v1/diary/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message_eng"], "Diary note not found.")
        self.assertEqual(response.data["message_chinese"], "未找到该日记。")

        # Note belonging to another user
        other_user = User.objects.create_user(
            email="otheruser2@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        other_note = DiaryNote.objects.create(
            user=other_user,
            icon="secret",
            date="2026-10-27",
            note="Confidential"
        )
        response_forbidden = self.client.get(f"/api/v1/diary/{other_note.id}/")
        self.assertEqual(response_forbidden.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_and_delete_diary_note(self):
        note = DiaryNote.objects.create(
            user=self.user,
            icon="old_icon",
            date="2026-10-27",
            note="Initial text"
        )
        detail_url = f"/api/v1/diary/{note.id}/"

        # Update
        update_res = self.client.put(detail_url, {"note": "Updated text"}, format="json")
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(update_res.data["message_eng"], "Diary note updated successfully.")
        self.assertEqual(update_res.data["message_chinese"], "日记更新成功。")
        self.assertEqual(update_res.data["data"]["note"], "Updated text")

        # Delete
        delete_res = self.client.delete(detail_url)
        self.assertEqual(delete_res.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_res.data["message_eng"], "Diary note deleted successfully.")
        self.assertEqual(delete_res.data["message_chinese"], "日记已成功删除。")
        self.assertFalse(DiaryNote.objects.filter(id=note.id).exists())

    def test_unauthenticated_requests_rejected(self):
        self.client.credentials()  # Clear auth
        res_get = self.client.get(self.list_create_url)
        self.assertEqual(res_get.status_code, status.HTTP_401_UNAUTHORIZED)

        res_post = self.client.post(self.list_create_url, {"icon": "test", "date": "2026-10-27", "note": "test"})
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)

