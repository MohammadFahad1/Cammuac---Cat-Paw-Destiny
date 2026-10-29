from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base import NewAPIView
from accounts.serializers import EmptySerializer
from .models import DailyCheckIn, Alarm, DayStatus, DayStatusType, get_day_status_payload, get_calendar_status_info
from .serializers import DailyCheckInSerializer, AlarmSerializer, AlarmCreateUpdateSerializer
from .choices import generate_random_daily_check_in, get_all_choices
from .calendar_generator import build_calendar_response_data

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
            "day_status": {
                "code": "lucky",
                "status": "Lucky",
                "en": "Lucky",
                "zh": "大吉",
                "name_en": "Lucky",
                "name_zh": "大吉"
            },
            "data": {
                "id": 1,
                "date": "2026-10-26",
                "day": 26,
                "month_year": "Oct 2026",
                "weekday_en": "Mon",
                "weekday_zh": "星期一",
                "day_status": {
                    "code": "lucky",
                    "status": "Lucky",
                    "en": "Lucky",
                    "zh": "大吉",
                    "name_en": "Lucky",
                    "name_zh": "大吉"
                },
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
            "day_status": {
                "code": "normal",
                "status": "Normal",
                "en": "Normal",
                "zh": "平",
                "name_en": "Normal",
                "name_zh": "平"
            },
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

        day_status_obj = DayStatus.objects.filter(date=today).first()
        status_key = day_status_obj.status if day_status_obj else DayStatusType.NORMAL
        day_status_data = get_day_status_payload(status_key)

        if record:
            return self.success_response(
                en_msg="Today's check-in retrieved successfully.",
                zh_msg="成功获取今日签到记录。",
                status_code=status.HTTP_200_OK,
                has_record=True,
                day_status=day_status_data,
                data=DailyCheckInSerializer(record).data
            )

        return self.success_response(
            en_msg="No check-in record found for today.",
            zh_msg="今日尚未签到。",
            status_code=status.HTTP_200_OK,
            has_record=False,
            day_status=day_status_data,
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
            "day_status": {
                "code": "lucky",
                "status": "Lucky",
                "en": "Lucky",
                "zh": "大吉",
                "name_en": "Lucky",
                "name_zh": "大吉"
            },
            "data": {
                "id": 1,
                "date": "2026-10-26",
                "day": 26,
                "month_year": "Oct 2026",
                "weekday_en": "Mon",
                "weekday_zh": "星期一",
                "day_status": {
                    "code": "lucky",
                    "status": "Lucky",
                    "en": "Lucky",
                    "zh": "大吉",
                    "name_en": "Lucky",
                    "name_zh": "大吉"
                },
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

        day_status_obj = DayStatus.objects.filter(date=today).first()
        status_key = day_status_obj.status if day_status_obj else DayStatusType.NORMAL
        day_status_data = get_day_status_payload(status_key)

        if existing_record:
            return self.error_response(
                "You have already checked in today. Check-in is allowed once a day.",
                "今日已完成签到，每天只能签到一次。",
                status_code=status.HTTP_400_BAD_REQUEST,
                has_record=True,
                day_status=day_status_data,
                data=DailyCheckInSerializer(existing_record).data
            )

        fortune_data = generate_random_daily_check_in()
        record = DailyCheckIn.objects.create(
            user=request.user,
            date=today,
            day_status=status_key,
            **fortune_data
        )

        return self.success_response(
            en_msg="Daily check-in completed successfully.",
            zh_msg="每日签到成功。",
            status_code=status.HTTP_201_CREATED,
            has_record=True,
            day_status=day_status_data,
            data=DailyCheckInSerializer(record).data
        )


class AlarmListCreateAPIView(NewAPIView):
    serializer_class = AlarmCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        tags=['Alarms'],
        responses={
            status.HTTP_200_OK: AlarmSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request):
        """
        **List User Alarms - Authenticated Users**

        Retrieves all alarms created by the authenticated user in the required format.
        Each user only sees their own alarms.

        **Method:** `GET`
        **Endpoint:** `/api/v1/daily-check-in/alarms/` (also `/api/v1/alarms/` and `/api/v1/activities/alarms/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Alarms retrieved successfully.",
                "zh": "成功获取闹钟列表。"
            },
            "message_eng": "Alarms retrieved successfully.",
            "message_chinese": "成功获取闹钟列表。",
            "count": 5,
            "data": [
                {
                    "id": "1",
                    "time": "04:30",
                    "period": "PM",
                    "titleZh": "起床囉！",
                    "titleEn": "Wake Up!",
                    "repeat": "每天 Every day",
                    "iconEmoji": "🌅🐱",
                    "bgColor": "bg-pink-50",
                    "borderColor": "border-pink-200",
                    "enabled": true
                },
                {
                    "id": "2",
                    "time": "12:00",
                    "period": "PM",
                    "titleZh": "午餐時間",
                    "titleEn": "Lunch Time",
                    "repeat": "週一 週二 週三 週四 週五 Mon Tue Wed Thu Fri",
                    "iconEmoji": "🍜🐱",
                    "bgColor": "bg-amber-50",
                    "borderColor": "border-amber-200",
                    "enabled": true
                }
            ]
        }
        ```
        """
        alarms = Alarm.objects.filter(user=request.user).order_by('id')
        data = AlarmSerializer(alarms, many=True).data

        return self.success_response(
            en_msg="Alarms retrieved successfully.",
            zh_msg="成功获取闹钟列表。",
            status_code=status.HTTP_200_OK,
            count=len(data),
            data=data
        )

    @swagger_auto_schema(
        tags=['Alarms'],
        request_body=AlarmCreateUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: AlarmSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def post(self, request):
        """
        **Create New Alarm - Authenticated Users**

        Creates a new user-specific alarm. Accepts both camelCase (`titleZh`, `iconEmoji`, etc.)
        and snake_case (`title_zh`, `icon_emoji`, etc.) in request payloads.

        **Method:** `POST`
        **Endpoint:** `/api/v1/daily-check-in/alarms/` (also `/api/v1/alarms/` and `/api/v1/activities/alarms/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body (JSON):**
        ```json
        {
            "time": "04:30",
            "period": "PM",
            "titleZh": "起床囉！",
            "titleEn": "Wake Up!",
            "repeat": "每天 Every day",
            "iconEmoji": "🌅🐱",
            "bgColor": "bg-pink-50",
            "borderColor": "border-pink-200",
            "enabled": true
        }
        ```

        **Response Body - 201 Created (JSON):**
        ```json
        {
            "success": true,
            "status_code": 201,
            "message": {
                "en": "Alarm created successfully.",
                "zh": "闹钟创建成功。"
            },
            "message_eng": "Alarm created successfully.",
            "message_chinese": "闹钟创建成功。",
            "data": {
                "id": "1",
                "time": "04:30",
                "period": "PM",
                "titleZh": "起床囉！",
                "titleEn": "Wake Up!",
                "repeat": "每天 Every day",
                "iconEmoji": "🌅🐱",
                "bgColor": "bg-pink-50",
                "borderColor": "border-pink-200",
                "enabled": true
            }
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alarm = serializer.save()

        return self.success_response(
            en_msg="Alarm created successfully.",
            zh_msg="闹钟创建成功。",
            status_code=status.HTTP_201_CREATED,
            data=AlarmSerializer(alarm).data
        )


class AlarmDetailAPIView(NewAPIView):
    serializer_class = AlarmCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def _get_alarm(self, request, pk):
        """
        Retrieves the alarm strictly belonging to the authenticated user.
        Ensures complete user isolation.
        """
        return Alarm.objects.filter(pk=pk, user=request.user).first()

    @swagger_auto_schema(
        tags=['Alarms'],
        responses={
            status.HTTP_200_OK: AlarmSerializer,
            status.HTTP_404_NOT_FOUND: 'Alarm not found',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request, pk):
        """
        **Get Alarm Details - Authenticated Users**

        Retrieves a specific alarm by ID for the authenticated user.
        Attempts to access another user's alarm will return `404 Not Found`.

        **Method:** `GET`
        **Endpoint:** `/api/v1/daily-check-in/alarms/<pk>/` (also `/api/v1/alarms/<pk>/`)
        """
        alarm = self._get_alarm(request, pk)
        if not alarm:
            return self.error_response(
                "Alarm not found.",
                "未找到该闹钟。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.success_response(
            en_msg="Alarm details retrieved successfully.",
            zh_msg="成功获取闹钟详情。",
            status_code=status.HTTP_200_OK,
            data=AlarmSerializer(alarm).data
        )

    @swagger_auto_schema(
        tags=['Alarms'],
        request_body=AlarmCreateUpdateSerializer,
        responses={
            status.HTTP_200_OK: AlarmSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Alarm not found'
        }
    )
    def put(self, request, pk):
        """
        **Update Entire Alarm - Authenticated Users**

        Replaces all fields of an existing alarm belonging to the authenticated user.
        Attempts to edit another user's alarm will return `404 Not Found`.

        **Method:** `PUT`
        **Endpoint:** `/api/v1/daily-check-in/alarms/<pk>/` (also `/api/v1/alarms/<pk>/`)
        """
        alarm = self._get_alarm(request, pk)
        if not alarm:
            return self.error_response(
                "Alarm not found.",
                "未找到该闹钟。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(alarm, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        alarm = serializer.save()

        return self.success_response(
            en_msg="Alarm updated successfully.",
            zh_msg="闹钟更新成功。",
            status_code=status.HTTP_200_OK,
            data=AlarmSerializer(alarm).data
        )

    @swagger_auto_schema(
        tags=['Alarms'],
        request_body=AlarmCreateUpdateSerializer,
        responses={
            status.HTTP_200_OK: AlarmSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Alarm not found'
        }
    )
    def patch(self, request, pk):
        """
        **Partially Update Alarm (e.g. Toggle Enabled) - Authenticated Users**

        Partially updates an alarm (e.g., toggling `{"enabled": false}`).
        Attempts to edit another user's alarm will return `404 Not Found`.

        **Method:** `PATCH`
        **Endpoint:** `/api/v1/daily-check-in/alarms/<pk>/` (also `/api/v1/alarms/<pk>/`)

        **Request Body Example - Toggle enabled (JSON):**
        ```json
        {
            "enabled": false
        }
        ```
        """
        alarm = self._get_alarm(request, pk)
        if not alarm:
            return self.error_response(
                "Alarm not found.",
                "未找到该闹钟。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(alarm, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        alarm = serializer.save()

        return self.success_response(
            en_msg="Alarm updated successfully.",
            zh_msg="闹钟更新成功。",
            status_code=status.HTTP_200_OK,
            data=AlarmSerializer(alarm).data
        )

    @swagger_auto_schema(
        tags=['Alarms'],
        responses={
            status.HTTP_200_OK: 'Alarm deleted successfully',
            status.HTTP_404_NOT_FOUND: 'Alarm not found'
        }
    )
    def delete(self, request, pk):
        """
        **Delete Alarm - Authenticated Users**

        Deletes an alarm belonging to the authenticated user.
        Attempts to delete another user's alarm will return `404 Not Found`.

        **Method:** `DELETE`
        **Endpoint:** `/api/v1/daily-check-in/alarms/<pk>/` (also `/api/v1/alarms/<pk>/`)
        """
        alarm = self._get_alarm(request, pk)
        if not alarm:
            return self.error_response(
                "Alarm not found.",
                "未找到该闹钟。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        alarm.delete()
        return self.success_response(
            en_msg="Alarm deleted successfully.",
            zh_msg="闹钟已成功删除。",
            status_code=status.HTTP_200_OK
        )


class CalendarAPIView(NewAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']

    @swagger_auto_schema(
        tags=['Daily Check-in'],
        manual_parameters=[
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description="Specific calendar year (e.g. 2026)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'month',
                openapi.IN_QUERY,
                description="Specific month 1-12 (used when year is specified)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'start_year',
                openapi.IN_QUERY,
                description="Start year for calendar range (default: 2026)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'end_year',
                openapi.IN_QUERY,
                description="End year for calendar range (default: 2030)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'lang',
                openapi.IN_QUERY,
                description="Language code: 'en' for English format (Ji, Ping, Xiong) or 'zh' for Chinese format (吉, 平, 凶)",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={
            status.HTTP_200_OK: 'Calendar data retrieved successfully',
            status.HTTP_400_BAD_REQUEST: 'Invalid parameters',
        }
    )
    def get(self, request):
        """
        **Get Calendar Day Statuses (2025 - 2030) - Public & Authenticated**

        Returns the day-by-day status calendar managed from the backend database (`DayStatus`).
        Provides both English format (`Ji`, `Ping`, `Xiong`) and Chinese format (`吉`, `平`, `凶`),
        as well as detailed bilingual objects per day.

        **Method:** `GET`
        **Endpoint:** `/api/v1/daily-check-in/calendar/`
        **Authentication:** Optional (`AllowAny`)

        **Query Parameters:**
        - `year` (optional): Filter to a specific year (e.g. `?year=2026`)
        - `month` (optional): Filter to a specific month 1-12 (e.g. `?year=2026&month=10`)
        - `start_year` (optional): Custom range start year (default: `2026`)
        - `end_year` (optional): Custom range end year (default: `2030`)
        - `lang` (optional): `'en'` or `'zh'` to simplify the `data` payload to that language

        **Response Body - 200 OK (Full Bilingual Calendar):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Calendar data retrieved successfully.",
                "zh": "成功获取日历数据。"
            },
            "message_eng": "Calendar data retrieved successfully.",
            "message_chinese": "成功获取日历数据。",
            "calendar_en": {
                "2026": {
                    "10": {
                        "1": "Ping", "2": "Ping", "3": "Ji", "4": "Ping", "5": "Xiong",
                        "6": "Ji", "7": "Ping", "8": "Xiong", "9": "Xiong", "10": "Ping",
                        "11": "Ji", "12": "Ping", "13": "Ji", "14": "Ping", "15": "Ping",
                        "16": "Ping", "17": "Xiong", "18": "Ping", "19": "Ping", "20": "Ji",
                        "21": "Xiong", "22": "Ping", "23": "Ji", "24": "Ping", "25": "Ji",
                        "26": "Ping", "27": "Ping", "28": "Xiong", "29": "Xiong", "30": "Ping", "31": "Ping"
                    },
                    "11": {
                        "1": "Ji", "2": "Xiong", "3": "Ping", "4": "Ji", "5": "Ping",
                        "6": "Xiong", "7": "Ping", "8": "Ping", "9": "Ping", "10": "Xiong",
                        "11": "Ping", "12": "Ping", "13": "Ping", "14": "Ping", "15": "Xiong",
                        "16": "Ji", "17": "Ji", "18": "Ping", "19": "Ping", "20": "Ping",
                        "21": "Ping", "22": "Xiong", "23": "Ping", "24": "Ji", "25": "Ji",
                        "26": "Ping", "27": "Xiong", "28": "Ping", "29": "Ji", "30": "Ping"
                    },
                    "12": {
                        "1": "Ping", "2": "Ping", "3": "Ping", "4": "Xiong", "5": "Ping",
                        "6": "Ji", "7": "Ping", "8": "Ji", "9": "Ping", "10": "Xiong",
                        "11": "Ping", "12": "Ji", "13": "Ping", "14": "Ji", "15": "Ping",
                        "16": "Xiong", "17": "Ji", "18": "Ji", "19": "Ping", "20": "Ji",
                        "21": "Xiong", "22": "Xiong", "23": "Ping", "24": "Ji", "25": "Ping",
                        "26": "Ping", "27": "Xiong", "28": "Xiong", "29": "Ji", "30": "Ping", "31": "Ping"
                    }
                }
            },
            "calendar_zh": {
                "2026": {
                    "10": {
                        "1": "平", "2": "平", "3": "吉", "4": "平", "5": "凶",
                        "6": "吉", "7": "平", "8": "凶", "9": "凶", "10": "平",
                        "11": "吉", "12": "平", "13": "吉", "14": "平", "15": "平",
                        "16": "平", "17": "凶", "18": "平", "19": "平", "20": "吉",
                        "21": "凶", "22": "平", "23": "吉", "24": "平", "25": "吉",
                        "26": "平", "27": "平", "28": "凶", "29": "凶", "30": "平", "31": "平"
                    },
                    "11": {
                        "1": "吉", "2": "凶", "3": "平", "4": "吉", "5": "平",
                        "6": "凶", "7": "平", "8": "平", "9": "平", "10": "凶",
                        "11": "平", "12": "平", "13": "平", "14": "平", "15": "凶",
                        "16": "吉", "17": "吉", "18": "平", "19": "平", "20": "平",
                        "21": "平", "22": "凶", "23": "平", "24": "吉", "25": "吉",
                        "26": "平", "27": "凶", "28": "平", "29": "吉", "30": "平"
                    },
                    "12": {
                        "1": "平", "2": "平", "3": "平", "4": "凶", "5": "平",
                        "6": "吉", "7": "平", "8": "吉", "9": "平", "10": "凶",
                        "11": "平", "12": "吉", "13": "平", "14": "吉", "15": "平",
                        "16": "凶", "17": "吉", "18": "吉", "19": "平", "20": "吉",
                        "21": "凶", "22": "凶", "23": "平", "24": "吉", "25": "平",
                        "26": "平", "27": "凶", "28": "凶", "29": "吉", "30": "平", "31": "平"
                    }
                }
            },
            "data": {
                "en": { "2026": { "10": { "1": "Ping", "2": "Ping", ... } } },
                "zh": { "2026": { "10": { "1": "平", "2": "平", ... } } },
                "calendar_en": { "2026": { "10": { "1": "Ping", "2": "Ping", ... } } },
                "calendar_zh": { "2026": { "10": { "1": "平", "2": "平", ... } } },
                "bilingual": {
                    "2026": {
                        "10": {
                            "1": {
                                "en": "Ping",
                                "zh": "平",
                                "code": "normal",
                                "status_en": "Normal",
                                "status_zh": "平"
                            }
                        }
                    }
                }
            }
        }
        ```
        """
        year_param = request.query_params.get('year')
        month_param = request.query_params.get('month')
        start_year_param = request.query_params.get('start_year')
        end_year_param = request.query_params.get('end_year')
        lang_param = (request.query_params.get('lang') or '').lower().strip()

        year = None
        month = None
        start_year = None
        end_year = None

        if year_param is not None:
            try:
                year = int(year_param)
                if not (2000 <= year <= 2100):
                    raise ValueError
            except ValueError:
                return self.error_response(
                    "Invalid year format. Must be an integer between 2000 and 2100.",
                    "年份格式无效，必须在 2000 至 2100 之间。",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        if month_param is not None:
            try:
                month = int(month_param)
                if not (1 <= month <= 12):
                    raise ValueError
            except ValueError:
                return self.error_response(
                    "Invalid month format. Must be an integer between 1 and 12.",
                    "月份格式无效，必须在 1 至 12 之间。",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        if start_year_param is not None:
            try:
                start_year = int(start_year_param)
                if not (2000 <= start_year <= 2100):
                    raise ValueError
            except ValueError:
                return self.error_response(
                    "Invalid year format. Must be an integer between 2000 and 2100.",
                    "年份格式无效，必须在 2000 至 2100 之间。",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        if end_year_param is not None:
            try:
                end_year = int(end_year_param)
                if not (2000 <= end_year <= 2100):
                    raise ValueError
            except ValueError:
                return self.error_response(
                    "Invalid year format. Must be an integer between 2000 and 2100.",
                    "年份格式无效，必须在 2000 至 2100 之间。",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        calendar_en, calendar_zh, calendar_bilingual = build_calendar_response_data(
            start_year=start_year,
            end_year=end_year,
            year=year,
            month=month,
        )

        if lang_param == 'en':
            data_payload = calendar_en
        elif lang_param == 'zh':
            data_payload = calendar_zh
        else:
            data_payload = {
                'en': calendar_en,
                'zh': calendar_zh,
                'calendar_en': calendar_en,
                'calendar_zh': calendar_zh,
                'bilingual': calendar_bilingual,
            }

        return self.success_response(
            en_msg="Calendar data retrieved successfully.",
            zh_msg="成功获取日历数据。",
            status_code=status.HTTP_200_OK,
            calendar_en=calendar_en,
            calendar_zh=calendar_zh,
            data=data_payload
        )


