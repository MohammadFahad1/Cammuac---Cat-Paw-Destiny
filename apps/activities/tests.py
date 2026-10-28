from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DailyCheckIn, Alarm, DayStatus, DayStatusType

User = get_user_model()


class DailyCheckInDayStatusAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="fortuneuser@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.today_url = "/api/v1/daily-check-in/today/"

    def test_default_day_status_normal_when_not_in_db(self):
        # Admin has NOT entered a DayStatus for today -> should default to Normal
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["has_record"])
        self.assertIn("day_status", response.data)

        day_status = response.data["day_status"]
        self.assertEqual(day_status["code"], "normal")
        self.assertEqual(day_status["status"], "Normal")
        self.assertEqual(day_status["zh"], "平")

    def test_admin_configured_lucky_day_status(self):
        today = timezone.localdate()
        # Admin manually enters today as Lucky in admin
        DayStatus.objects.create(date=today, status=DayStatusType.LUCKY)

        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        day_status = response.data["day_status"]
        self.assertEqual(day_status["code"], "lucky")
        self.assertEqual(day_status["status"], "Lucky")
        self.assertEqual(day_status["zh"], "大吉")

    def test_admin_configured_bad_luck_day_status(self):
        today = timezone.localdate()
        # Admin manually enters today as Bad Luck in admin
        DayStatus.objects.create(date=today, status=DayStatusType.BAD_LUCK)

        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        day_status = response.data["day_status"]
        self.assertEqual(day_status["code"], "bad_luck")
        self.assertEqual(day_status["status"], "Bad Luck")
        self.assertEqual(day_status["zh"], "凶")

    def test_post_check_in_reflects_and_saves_day_status(self):
        today = timezone.localdate()
        # Admin set today as Lucky
        DayStatus.objects.create(date=today, status=DayStatusType.LUCKY)

        post_res = self.client.post(self.today_url, {}, format="json")
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post_res.data["has_record"])

        # Check top-level day_status
        self.assertEqual(post_res.data["day_status"]["code"], "lucky")
        self.assertEqual(post_res.data["day_status"]["status"], "Lucky")

        # Check data.day_status inside checkin payload
        data = post_res.data["data"]
        self.assertIn("day_status", data)
        self.assertEqual(data["day_status"]["code"], "lucky")
        self.assertEqual(data["day_status"]["status"], "Lucky")

        # Verify DB checkin model has day_status recorded
        record = DailyCheckIn.objects.get(user=self.user, date=today)
        self.assertEqual(record.day_status, "lucky")

        # Now GET should also return the Lucky day_status inside data and root
        get_res = self.client.get(self.today_url)
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertTrue(get_res.data["has_record"])
        self.assertEqual(get_res.data["day_status"]["status"], "Lucky")
        self.assertEqual(get_res.data["data"]["day_status"]["status"], "Lucky")


class AlarmAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="alarmuser@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.list_create_url = "/api/v1/daily-check-in/alarms/"

    def test_list_alarms_initially_empty(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["data"], [])
        self.assertEqual(response.data["message_eng"], "Alarms retrieved successfully.")
        self.assertEqual(response.data["message_chinese"], "成功获取闹钟列表。")

    def test_create_alarm_camel_case_format(self):
        payload = {
            "time": "04:30",
            "period": "PM",
            "titleZh": "起床囉！",
            "titleEn": "Wake Up!",
            "repeat": "每天 Every day",
            "iconEmoji": "🌅🐱",
            "bgColor": "bg-pink-50",
            "borderColor": "border-pink-200",
            "enabled": True,
        }
        response = self.client.post(self.list_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message_eng"], "Alarm created successfully.")
        self.assertEqual(response.data["message_chinese"], "闹钟创建成功。")

        data = response.data["data"]
        self.assertEqual(data["time"], "04:30")
        self.assertEqual(data["period"], "PM")
        self.assertEqual(data["titleZh"], "起床囉！")
        self.assertEqual(data["titleEn"], "Wake Up!")
        self.assertEqual(data["repeat"], "每天 Every day")
        self.assertEqual(data["iconEmoji"], "🌅🐱")
        self.assertEqual(data["bgColor"], "bg-pink-50")
        self.assertEqual(data["borderColor"], "border-pink-200")
        self.assertTrue(data["enabled"])
        self.assertIsInstance(data["id"], str)
        self.assertEqual(set(data.keys()), {
            "id", "time", "period", "titleZh", "titleEn",
            "repeat", "iconEmoji", "bgColor", "borderColor", "enabled"
        })

        # Verify DB
        alarm = Alarm.objects.get(id=int(data["id"]))
        self.assertEqual(alarm.user, self.user)
        self.assertEqual(alarm.title_zh, "起床囉！")

    def test_create_alarm_snake_case_compatibility(self):
        payload = {
            "time": "12:00",
            "period": "PM",
            "title_zh": "午餐時間",
            "title_en": "Lunch Time",
            "repeat": "週一 週二 週三 週四 週五 Mon Tue Wed Thu Fri",
            "icon_emoji": "🍜🐱",
            "bg_color": "bg-amber-50",
            "border_color": "border-amber-200",
            "enabled": True,
        }
        response = self.client.post(self.list_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data["data"]
        self.assertEqual(data["titleZh"], "午餐時間")
        self.assertEqual(data["titleEn"], "Lunch Time")
        self.assertEqual(data["iconEmoji"], "🍜🐱")

    def test_get_alarm_detail_success(self):
        alarm = Alarm.objects.create(
            user=self.user,
            time="03:00",
            period="PM",
            title_zh="休息一下",
            title_en="Take a Break",
            repeat="每天 Every day",
            icon_emoji="😴🐱",
            bg_color="bg-orange-50",
            border_color="border-orange-200",
            enabled=True
        )
        detail_url = f"{self.list_create_url}{alarm.id}/"
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["id"], str(alarm.id))
        self.assertEqual(response.data["data"]["titleZh"], "休息一下")
        self.assertEqual(response.data["data"]["titleEn"], "Take a Break")

    def test_update_alarm_put(self):
        alarm = Alarm.objects.create(
            user=self.user,
            time="08:00",
            period="PM",
            title_zh="放鬆時光",
            title_en="Relax Time",
            repeat="每天 Every day",
            icon_emoji="👓🐱",
            bg_color="bg-sky-50",
            border_color="border-sky-200",
            enabled=False
        )
        detail_url = f"{self.list_create_url}{alarm.id}/"
        payload = {
            "time": "09:00",
            "period": "PM",
            "titleZh": "放鬆時光（更新）",
            "titleEn": "Relax Time (Updated)",
            "repeat": "週末 Weekend",
            "iconEmoji": "👓🐱",
            "bgColor": "bg-sky-100",
            "borderColor": "border-sky-300",
            "enabled": True
        }
        response = self.client.put(detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message_eng"], "Alarm updated successfully.")
        self.assertEqual(response.data["message_chinese"], "闹钟更新成功。")
        self.assertEqual(response.data["data"]["time"], "09:00")
        self.assertTrue(response.data["data"]["enabled"])

    def test_patch_alarm_toggle_enabled(self):
        alarm = Alarm.objects.create(
            user=self.user,
            time="11:00",
            period="PM",
            title_zh="晚安",
            title_en="Good Night",
            enabled=True
        )
        detail_url = f"{self.list_create_url}{alarm.id}/"

        # Toggle enabled to False
        patch_res = self.client.patch(detail_url, {"enabled": False}, format="json")
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertFalse(patch_res.data["data"]["enabled"])

        alarm.refresh_from_db()
        self.assertFalse(alarm.enabled)

    def test_delete_alarm_success(self):
        alarm = Alarm.objects.create(
            user=self.user,
            time="06:00",
            period="AM",
            title_zh="晨跑",
            title_en="Morning Run"
        )
        detail_url = f"{self.list_create_url}{alarm.id}/"
        del_res = self.client.delete(detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)
        self.assertEqual(del_res.data["message_eng"], "Alarm deleted successfully.")
        self.assertEqual(del_res.data["message_chinese"], "闹钟已成功删除。")
        self.assertFalse(Alarm.objects.filter(id=alarm.id).exists())

    def test_user_isolation(self):
        other_user = User.objects.create_user(
            email="otheruser@example.com",
            password="StrongPassword123!",
            is_active=True,
            status=User.ACTIVE
        )
        other_alarm = Alarm.objects.create(
            user=other_user,
            time="07:00",
            period="AM",
            title_zh="他人闹钟",
            title_en="Other Alarm",
            enabled=True
        )

        # GET list should NOT include other_user's alarm
        list_res = self.client.get(self.list_create_url)
        self.assertEqual(list_res.data["count"], 0)

        # GET detail of other_user's alarm -> 404
        detail_res = self.client.get(f"{self.list_create_url}{other_alarm.id}/")
        self.assertEqual(detail_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(detail_res.data["message_eng"], "Alarm not found.")
        self.assertEqual(detail_res.data["message_chinese"], "未找到该闹钟。")

        # PUT on other_user's alarm -> 404
        put_res = self.client.put(f"{self.list_create_url}{other_alarm.id}/", {"time": "08:00"}, format="json")
        self.assertEqual(put_res.status_code, status.HTTP_404_NOT_FOUND)

        # PATCH on other_user's alarm -> 404
        patch_res = self.client.patch(f"{self.list_create_url}{other_alarm.id}/", {"enabled": False}, format="json")
        self.assertEqual(patch_res.status_code, status.HTTP_404_NOT_FOUND)

        # DELETE on other_user's alarm -> 404
        del_res = self.client.delete(f"{self.list_create_url}{other_alarm.id}/")
        self.assertEqual(del_res.status_code, status.HTTP_404_NOT_FOUND)

        other_alarm.refresh_from_db()
        self.assertTrue(other_alarm.enabled)

    def test_unauthenticated_requests_rejected(self):
        self.client.credentials()  # Clear auth
        res_get = self.client.get(self.list_create_url)
        self.assertEqual(res_get.status_code, status.HTTP_401_UNAUTHORIZED)

        res_post = self.client.post(self.list_create_url, {"time": "04:30"})
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)
