from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from core.base import NewAPIView
from accounts.serializers import EmptySerializer
from .models import CatTarotDraw
from .serializers import CatTarotDrawSerializer, CatTarotDrawInputSerializer
from .choices import get_random_tarot_card

class TodayCatTarotAPIView(NewAPIView):
    serializer_class = CatTarotDrawInputSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        tags=['Cat Tarot (Card)'],
        responses={
            status.HTTP_200_OK: CatTarotDrawSerializer,
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request):
        """
        **Get Today's Cat Tarot Reading - Authenticated Users**

        Checks if the authenticated user has already drawn a Cat Tarot card for the current date.
        - If a card has been drawn today, returns `has_record: true` and the tarot details including the selected `card_number` (1, 2, or 3).
        - If no card has been drawn today, returns `has_record: false` and `data: null`.

        **Method:** `GET`
        **Endpoint:** `/api/v1/tarot/today/` (also `/api/v1/cat-tarot/today/` and `/api/v1/tarot/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (When Tarot Drawn Today):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Today's cat tarot retrieved successfully.",
                "zh": "成功获取今日猫咪塔罗指引。"
            },
            "message_eng": "Today's cat tarot retrieved successfully.",
            "message_chinese": "成功获取今日猫咪塔罗指引。",
            "has_record": true,
            "data": {
                "id": 1,
                "card_number": 2,
                "date": "2026-10-27",
                "day": 27,
                "month_year": "Oct 2026",
                "weekday_en": "Tue",
                "weekday_zh": "星期二",
                "category": {
                    "en": "Today's Guidance",
                    "zh": "今日指引"
                },
                "tag": {
                    "en": "Today's Guidance",
                    "zh": "今日指引"
                },
                "title": {
                    "en": "A New Beginning",
                    "zh": "新的開始"
                },
                "content": {
                    "en": "Today is a great time to start fresh. Let go of past worries, embrace new possibilities, and good fortune is coming your way.",
                    "zh": "今天是重新出發的好時機。放下過去的擔憂，勇敢迎接新的可能性，幸運正在靠近你。"
                },
                "created_at": "2026-10-27T09:30:00Z",
                "updated_at": "2026-10-27T09:30:00Z"
            }
        }
        ```

        **Response Body - 200 OK (When Not Yet Drawn Today):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "No cat tarot record found for today.",
                "zh": "今日尚未抽取猫咪塔罗。"
            },
            "message_eng": "No cat tarot record found for today.",
            "message_chinese": "今日尚未抽取猫咪塔罗。",
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
        record = CatTarotDraw.objects.filter(user=request.user, date=today).first()

        if record:
            return self.success_response(
                en_msg="Today's cat tarot retrieved successfully.",
                zh_msg="成功获取今日猫咪塔罗指引。",
                status_code=status.HTTP_200_OK,
                has_record=True,
                data=CatTarotDrawSerializer(record).data
            )

        return self.success_response(
            en_msg="No cat tarot record found for today.",
            zh_msg="今日尚未抽取猫咪塔罗。",
            status_code=status.HTTP_200_OK,
            has_record=False,
            data=None
        )

    @swagger_auto_schema(
        tags=['Cat Tarot (Card)'],
        request_body=CatTarotDrawInputSerializer,
        responses={
            status.HTTP_201_CREATED: CatTarotDrawSerializer,
            status.HTTP_400_BAD_REQUEST: 'Already drawn today or invalid card number',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def post(self, request):
        """
        **Draw Today's Cat Tarot Card - Authenticated Users**

        Allows the user to select one of three cards (`card_number`: 1, 2, or 3) **once every calendar day**.
        Randomly assigns a guidance reading from the pre-defined Cat Tarot pool and saves it for today.
        Subsequent draw attempts on the same calendar day will be rejected with `400 Bad Request`.

        **Method:** `POST`
        **Endpoint:** `/api/v1/tarot/today/` (also `/api/v1/cat-tarot/today/` and `/api/v1/tarot/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body (JSON):**
        ```json
        {
            "card_number": 2
        }
        ```

        **Response Body - 201 Created:**
        ```json
        {
            "success": true,
            "status_code": 201,
            "message": {
                "en": "Cat tarot drawn successfully.",
                "zh": "猫咪塔罗抽取成功。"
            },
            "message_eng": "Cat tarot drawn successfully.",
            "message_chinese": "猫咪塔罗抽取成功。",
            "has_record": true,
            "data": {
                "id": 1,
                "card_number": 2,
                "date": "2026-10-27",
                "day": 27,
                "month_year": "Oct 2026",
                "weekday_en": "Tue",
                "weekday_zh": "星期二",
                "category": {
                    "en": "Today's Guidance",
                    "zh": "今日指引"
                },
                "tag": {
                    "en": "Today's Guidance",
                    "zh": "今日指引"
                },
                "title": {
                    "en": "A New Beginning",
                    "zh": "新的開始"
                },
                "content": {
                    "en": "Today is a great time to start fresh. Let go of past worries, embrace new possibilities, and good fortune is coming your way.",
                    "zh": "今天是重新出發的好時機。放下過去的擔憂，勇敢迎接新的可能性，幸運正在靠近你。"
                },
                "created_at": "2026-10-27T09:30:00Z",
                "updated_at": "2026-10-27T09:30:00Z"
            }
        }
        ```

        **Response Body - 400 Bad Request (Already Drawn Today):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "You have already drawn a cat tarot card today. Tarot draw is allowed once a day.",
                "zh": "今日已抽取猫咪塔罗，每天只能抽取一次。"
            },
            "message_eng": "You have already drawn a cat tarot card today. Tarot draw is allowed once a day.",
            "message_chinese": "今日已抽取猫咪塔罗，每天只能抽取一次。",
            "has_record": true,
            "data": { ... }
        }
        ```

        **Response Body - 400 Bad Request (Invalid Card Number):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "card_number: Ensure this value is less than or equal to 3.",
                "zh": "卡片编号: 确保该值小于或等于 3。"
            },
            "message_eng": "card_number: Ensure this value is less than or equal to 3.",
            "message_chinese": "卡片编号: 确保该值小于或等于 3。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_number = serializer.validated_data['card_number']
        today = timezone.localdate()

        existing_record = CatTarotDraw.objects.filter(user=request.user, date=today).first()
        if existing_record:
            return self.error_response(
                "You have already drawn a cat tarot card today. Tarot draw is allowed once a day.",
                "今日已抽取猫咪塔罗，每天只能抽取一次。",
                status_code=status.HTTP_400_BAD_REQUEST,
                has_record=True,
                data=CatTarotDrawSerializer(existing_record).data
            )

        tarot_card = get_random_tarot_card()
        record = CatTarotDraw.objects.create(
            user=request.user,
            date=today,
            card_number=card_number,
            category_en=tarot_card["category"]["en"],
            category_zh=tarot_card["category"]["zh"],
            title_en=tarot_card["title"]["en"],
            title_zh=tarot_card["title"]["zh"],
            content_en=tarot_card["content"]["en"],
            content_zh=tarot_card["content"]["zh"],
        )

        return self.success_response(
            en_msg="Cat tarot drawn successfully.",
            zh_msg="猫咪塔罗抽取成功。",
            status_code=status.HTTP_201_CREATED,
            has_record=True,
            data=CatTarotDrawSerializer(record).data
        )

