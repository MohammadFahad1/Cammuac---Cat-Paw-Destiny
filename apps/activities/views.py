from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from core.base import NewAPIView
from accounts.serializers import EmptySerializer
from .models import DailyCheckIn
from .serializers import DailyCheckInSerializer
from .choices import generate_random_daily_check_in, get_all_choices

class TodayCheckInAPIView(NewAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        tags=['Daily Check-in'],
        responses={
            status.HTTP_200_OK: DailyCheckInSerializer,
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request):
        """
        **Get Today's Daily Check-in - Authenticated Users**

        Checks if a daily check-in / cat fortune record already exists for the authenticated user for the current date.
        If a record exists, returns the check-in details with `has_record: true`.
        If no record exists, returns `has_record: false` and `data: null`.

        **Method:** `GET`
        **Endpoint:** `/api/v1/daily-check-in/today/` (also `/api/v1/activities/today/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (When Check-in Exists):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Today's check-in retrieved successfully.",
                "zh": "成功获取今日签到记录。"
            },
            "message_eng": "Today's check-in retrieved successfully.",
            "message_chinese": "成功获取今日签到记录。",
            "has_record": true,
            "data": {
                "id": 1,
                "date": "2026-10-26",
                "day": 26,
                "month_year": "Oct 2026",
                "weekday_en": "Mon",
                "weekday_zh": "星期一",
                "good_for": {
                    "en": "Effort, Smiles, Learning",
                    "zh": "努力、微笑、學習",
                    "items_en": ["Effort", "Smiles", "Learning"],
                    "items_zh": ["努力", "微笑", "學習"]
                },
                "avoid": {
                    "en": "Anxiety, Comparison, Staying up late",
                    "zh": "焦慮、比較、熬夜",
                    "items_en": ["Anxiety", "Comparison", "Staying up late"],
                    "items_zh": ["焦慮", "比較", "熬夜"]
                },
                "quote": {
                    "en": "An ordinary day can still make an extraordinary you.",
                    "zh": "平凡的一天，也能成就很不平凡的你。"
                },
                "lucky_color": {
                    "name_en": "Pink",
                    "name_zh": "粉色",
                    "hex": "#FF69B4"
                },
                "lucky_number": 7,
                "lucky_direction": {
                    "code": "SE",
                    "name_en": "Southeast",
                    "name_zh": "東南"
                },
                "created_at": "2026-10-26T16:30:00Z",
                "updated_at": "2026-10-26T16:30:00Z"
            }
        }
        ```

        **Response Body - 200 OK (When Not Yet Checked In Today):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "No check-in record found for today.",
                "zh": "今日尚未签到。"
            },
            "message_eng": "No check-in record found for today.",
            "message_chinese": "今日尚未签到。",
            "has_record": false,
            "data": null
        }
        ```

        **Response Body - 401 Unauthorized:**
        ```json
        {
            "success": false,
            "status_code": 401,
            "message": {
                "en": "Authentication credentials were not provided.",
                "zh": "未提供身份验证凭据。"
            },
            "message_eng": "Authentication credentials were not provided.",
            "message_chinese": "未提供身份验证凭据。"
        }
        ```
        """
        today = timezone.localdate()
        record = DailyCheckIn.objects.filter(user=request.user, date=today).first()

        if record:
            return self.success_response(
                en_msg="Today's check-in retrieved successfully.",
                zh_msg="成功获取今日签到记录。",
                status_code=status.HTTP_200_OK,
                has_record=True,
                data=DailyCheckInSerializer(record).data
            )

        return self.success_response(
            en_msg="No check-in record found for today.",
            zh_msg="今日尚未签到。",
            status_code=status.HTTP_200_OK,
            has_record=False,
            data=None
        )

    @swagger_auto_schema(
        tags=['Daily Check-in'],
        request_body=EmptySerializer,
        responses={
            status.HTTP_201_CREATED: DailyCheckInSerializer,
            status.HTTP_400_BAD_REQUEST: 'Already checked in today',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def post(self, request):
        """
        **Complete Today's Daily Check-in - Authenticated Users**

        Performs daily check-in and generates today's cat fortune record for the authenticated user.
        Randomly selects items from pre-defined choices:
        - 3 Good-for items (宜)
        - 3 Avoid items (忌)
        - 1 Motivational quote
        - 1 Lucky color (with hex)
        - 1 Lucky number
        - 1 Lucky direction

        A user can only check in **once per calendar day**.
        Subsequent calls on the same day will be rejected with `400 Bad Request`.

        **Method:** `POST`
        **Endpoint:** `/api/v1/daily-check-in/today/` (also `/api/v1/activities/today/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None (or `{}`)

        **Response Body - 201 Created:**
        ```json
        {
            "success": true,
            "status_code": 201,
            "message": {
                "en": "Daily check-in completed successfully.",
                "zh": "每日签到成功。"
            },
            "message_eng": "Daily check-in completed successfully.",
            "message_chinese": "每日签到成功。",
            "has_record": true,
            "data": {
                "id": 1,
                "date": "2026-10-26",
                "day": 26,
                "month_year": "Oct 2026",
                "weekday_en": "Mon",
                "weekday_zh": "星期一",
                "good_for": {
                    "en": "Effort, Smiles, Learning",
                    "zh": "努力、微笑、學習",
                    "items_en": ["Effort", "Smiles", "Learning"],
                    "items_zh": ["努力", "微笑", "學習"]
                },
                "avoid": {
                    "en": "Anxiety, Comparison, Staying up late",
                    "zh": "焦慮、比較、熬夜",
                    "items_en": ["Anxiety", "Comparison", "Staying up late"],
                    "items_zh": ["焦慮", "比較", "熬夜"]
                },
                "quote": {
                    "en": "An ordinary day can still make an extraordinary you.",
                    "zh": "平凡的一天，也能成就很不平凡的你。"
                },
                "lucky_color": {
                    "name_en": "Pink",
                    "name_zh": "粉色",
                    "hex": "#FF69B4"
                },
                "lucky_number": 7,
                "lucky_direction": {
                    "code": "SE",
                    "name_en": "Southeast",
                    "name_zh": "東南"
                },
                "created_at": "2026-10-26T16:30:00Z",
                "updated_at": "2026-10-26T16:30:00Z"
            }
        }
        ```

        **Response Body - 400 Bad Request (Already Checked In Today):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "You have already checked in today. Check-in is allowed once a day.",
                "zh": "今日已完成签到，每天只能签到一次。"
            },
            "message_eng": "You have already checked in today. Check-in is allowed once a day.",
            "message_chinese": "今日已完成签到，每天只能签到一次。"
        }
        ```
        """
        today = timezone.localdate()
        existing_record = DailyCheckIn.objects.filter(user=request.user, date=today).first()

        if existing_record:
            return self.error_response(
                "You have already checked in today. Check-in is allowed once a day.",
                "今日已完成签到，每天只能签到一次。",
                status_code=status.HTTP_400_BAD_REQUEST,
                has_record=True,
                data=DailyCheckInSerializer(existing_record).data
            )

        fortune_data = generate_random_daily_check_in()
        record = DailyCheckIn.objects.create(
            user=request.user,
            date=today,
            **fortune_data
        )

        return self.success_response(
            en_msg="Daily check-in completed successfully.",
            zh_msg="每日签到成功。",
            status_code=status.HTTP_201_CREATED,
            has_record=True,
            data=DailyCheckInSerializer(record).data
        )
