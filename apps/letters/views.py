from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base import NewAPIView
from .models import Letter, LetterStatus
from .serializers import LetterSerializer, LetterCreateSerializer, LetterUpdateSerializer

class LetterListCreateAPIView(NewAPIView):
    serializer_class = LetterCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        tags=['My Letters'],
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by letter status: 'all', 'pending' (待開啟), or 'opened' (已開啟)",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            status.HTTP_200_OK: LetterSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request):
        """
        **List My Letters - Authenticated Users**

        Retrieves all letters written to the future self by the authenticated user.
        Supports filtering by status (`pending`, `opened`, or `all`).
        Also returns overview counters (`total_count`, `pending_count`, `opened_count`).

        **Method:** `GET`
        **Endpoint:** `/api/v1/letters/` (also `/api/v1/my-letters/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Query Parameters:**
        - `status` (optional): `all` (default), `pending` (待開啟), or `opened` (已開啟)

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Letters retrieved successfully.",
                "zh": "成功获取信件列表。"
            },
            "message_eng": "Letters retrieved successfully.",
            "message_chinese": "成功获取信件列表。",
            "total_count": 3,
            "pending_count": 2,
            "opened_count": 1,
            "data": [
                {
                    "id": 1,
                    "sticker": "bear",
                    "title": "未來的我，你好！",
                    "content": "希望那時候的我，已經實現了現在的夢想...",
                    "status": "pending",
                    "status_display": {
                        "en": "Pending",
                        "zh": "待開啟"
                    },
                    "is_opened": false,
                    "date": "2026-10-27",
                    "formatted_date_zh": "2026年10月27日",
                    "formatted_date_en": "October 27, 2026",
                    "content_length": 128,
                    "opened_at": null,
                    "created_at": "2026-10-27T10:00:00Z",
                    "updated_at": "2026-10-27T10:00:00Z"
                }
            ]
        }
        ```
        """
        base_queryset = Letter.objects.filter(user=request.user)

        total_count = base_queryset.count()
        pending_count = base_queryset.filter(status=LetterStatus.PENDING).count()
        opened_count = base_queryset.filter(status=LetterStatus.OPENED).count()

        status_filter = request.query_params.get('status', '').strip().lower()
        if status_filter == LetterStatus.PENDING:
            queryset = base_queryset.filter(status=LetterStatus.PENDING)
        elif status_filter == LetterStatus.OPENED:
            queryset = base_queryset.filter(status=LetterStatus.OPENED)
        else:
            queryset = base_queryset

        serialized_data = LetterSerializer(queryset, many=True).data

        return self.success_response(
            en_msg="Letters retrieved successfully.",
            zh_msg="成功获取信件列表。",
            status_code=status.HTTP_200_OK,
            total_count=total_count,
            pending_count=pending_count,
            opened_count=opened_count,
            data=serialized_data
        )

    @swagger_auto_schema(
        tags=['My Letters'],
        request_body=LetterCreateSerializer,
        responses={
            status.HTTP_201_CREATED: LetterSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def post(self, request):
        """
        **Create / Save a Letter to Future Self - Authenticated Users**

        Creates a new letter to future self.
        Newly created letters are initialized with status `pending` (待開啟).

        **Method:** `POST`
        **Endpoint:** `/api/v1/letters/` (also `/api/v1/my-letters/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body (JSON):**
        ```json
        {
            "sticker": "bear",
            "title": "未來的我，你好！",
            "content": "希望那時候的我，已經實現了現在的夢想，不管遇到什麼困難，都不要放棄。"
        }
        ```
        *(Both `sticker` and `title` are optional; `content` is required up to 1000-2000 chars)*

        **Response Body - 201 Created (JSON):**
        ```json
        {
            "success": true,
            "status_code": 201,
            "message": {
                "en": "Letter saved successfully.",
                "zh": "信件保存成功。"
            },
            "message_eng": "Letter saved successfully.",
            "message_chinese": "信件保存成功。",
            "data": {
                "id": 1,
                "sticker": "bear",
                "title": "未來的我，你好！",
                "content": "希望那時候的我，已經實現了現在的夢想，不管遇到什麼困難，都不要放棄。",
                "status": "pending",
                "status_display": {
                    "en": "Pending",
                    "zh": "待開啟"
                },
                "is_opened": false,
                "date": "2026-10-27",
                "formatted_date_zh": "2026年10月27日",
                "formatted_date_en": "October 27, 2026",
                "content_length": 34,
                "opened_at": null,
                "created_at": "2026-10-27T10:15:00Z",
                "updated_at": "2026-10-27T10:15:00Z"
            }
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title') or "未來的我，你好！"
        sticker = serializer.validated_data.get('sticker') or "heart"
        content = serializer.validated_data['content']

        letter = Letter.objects.create(
            user=request.user,
            sticker=sticker,
            title=title,
            content=content,
            status=LetterStatus.PENDING,
            date=timezone.localdate()
        )

        return self.success_response(
            en_msg="Letter saved successfully.",
            zh_msg="信件保存成功。",
            status_code=status.HTTP_201_CREATED,
            data=LetterSerializer(letter).data
        )


class LetterDetailAPIView(NewAPIView):
    serializer_class = LetterUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def _get_letter(self, request, pk):
        """
        Retrieves the letter strictly belonging to the authenticated user.
        Ensures complete user-isolation (cannot access other users' letters).
        """
        return Letter.objects.filter(pk=pk, user=request.user).first()

    @swagger_auto_schema(
        tags=['My Letters'],
        responses={
            status.HTTP_200_OK: LetterSerializer,
            status.HTTP_404_NOT_FOUND: 'Letter not found',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request, pk):
        """
        **Get Letter Details & Mark as Opened - Authenticated Users**

        Retrieves the details of a specific letter belonging to the authenticated user.
        **Special Feature:** If the letter is currently in `pending` status, opening it via this endpoint
        **automatically updates its status to `opened` (已開啟)** and records `opened_at` timestamp.

        **Method:** `GET`
        **Endpoint:** `/api/v1/letters/<pk>/` (also `/api/v1/my-letters/<pk>/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Letter retrieved successfully.",
                "zh": "成功获取信件详情。"
            },
            "message_eng": "Letter retrieved successfully.",
            "message_chinese": "成功获取信件详情。",
            "data": {
                "id": 1,
                "sticker": "bear",
                "title": "未來的我，你好！",
                "content": "希望那時候的我，已經實現了現在的夢想，不管遇到什麼困難，都不要放棄。要成為更勇敢、更自律、更快樂的人。記得保持熱愛，繼續努力，因為未來的你，一定會感謝現在這麼努力的自己！",
                "status": "opened",
                "status_display": {
                    "en": "Opened",
                    "zh": "已開啟"
                },
                "is_opened": true,
                "date": "2026-10-27",
                "formatted_date_zh": "2026年10月27日",
                "formatted_date_en": "October 27, 2026",
                "content_length": 87,
                "opened_at": "2026-10-27T10:20:00Z",
                "created_at": "2026-10-27T10:15:00Z",
                "updated_at": "2026-10-27T10:20:00Z"
            }
        }
        ```

        **Response Body - 404 Not Found (JSON):**
        ```json
        {
            "success": false,
            "status_code": 404,
            "message": {
                "en": "Letter not found.",
                "zh": "未找到该信件。"
            },
            "message_eng": "Letter not found.",
            "message_chinese": "未找到该信件。"
        }
        ```
        """
        letter = self._get_letter(request, pk)
        if not letter:
            return self.error_response(
                "Letter not found.",
                "未找到该信件。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Update status to 'opened' when viewed
        if letter.status == LetterStatus.PENDING:
            letter.mark_as_opened()

        return self.success_response(
            en_msg="Letter retrieved successfully.",
            zh_msg="成功获取信件详情。",
            status_code=status.HTTP_200_OK,
            data=LetterSerializer(letter).data
        )

    @swagger_auto_schema(
        tags=['My Letters'],
        request_body=LetterUpdateSerializer,
        responses={
            status.HTTP_200_OK: LetterSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Letter not found',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def put(self, request, pk):
        """
        **Replace / Update Letter - Authenticated Users**

        Updates all fields of an existing letter (sticker, title, content, and optional status) belonging to the authenticated user.
        Attempts to update another user's letter will return `404 Not Found`.

        **Method:** `PUT`
        **Endpoint:** `/api/v1/letters/<pk>/` (also `/api/v1/my-letters/<pk>/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body (JSON):**
        ```json
        {
            "sticker": "bear",
            "title": "未來的我，你好！",
            "content": "希望那時候的我，已經實現了現在的夢想，不管遇到什麼困難，都不要放棄。",
            "status": "opened"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Letter updated successfully.",
                "zh": "信件更新成功。"
            },
            "message_eng": "Letter updated successfully.",
            "message_chinese": "信件更新成功。",
            "data": {
                "id": 1,
                "sticker": "bear",
                "title": "未來的我，你好！",
                "content": "希望那時候的我，已經實現了現在的夢想，不管遇到什麼困難，都不要放棄。",
                "status": "opened",
                "status_display": {
                    "en": "Opened",
                    "zh": "已開啟"
                },
                "is_opened": true,
                "date": "2026-10-27",
                "formatted_date_zh": "2026年10月27日",
                "formatted_date_en": "October 27, 2026",
                "content_length": 34,
                "opened_at": "2026-10-27T10:20:00Z",
                "created_at": "2026-10-27T10:15:00Z",
                "updated_at": "2026-10-27T10:35:00Z"
            }
        }
        ```

        **Response Body - 404 Not Found (JSON):**
        ```json
        {
            "success": false,
            "status_code": 404,
            "message": {
                "en": "Letter not found.",
                "zh": "未找到该信件。"
            },
            "message_eng": "Letter not found.",
            "message_chinese": "未找到该信件。"
        }
        ```
        """
        return self._update_letter(request, pk, partial=False)

    @swagger_auto_schema(
        tags=['My Letters'],
        request_body=LetterUpdateSerializer,
        responses={
            status.HTTP_200_OK: LetterSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Letter not found',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def patch(self, request, pk):
        """
        **Partially Update Letter or Status - Authenticated Users**

        Partially updates an existing letter belonging to the authenticated user.
        Supports updating the status directly to `pending` (待開啟) or `opened` (已開啟),
        as well as modifying individual fields (`sticker`, `title`, `content`).
        Attempts to update another user's letter will return `404 Not Found`.

        **Method:** `PATCH`
        **Endpoint:** `/api/v1/letters/<pk>/` (also `/api/v1/my-letters/<pk>/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body - Example 1: Update Status to Opened (JSON):**
        ```json
        {
            "status": "opened"
        }
        ```

        **Request Body - Example 2: Revert Status to Pending (JSON):**
        ```json
        {
            "status": "pending"
        }
        ```

        **Request Body - Example 3: Update Title and Content (JSON):**
        ```json
        {
            "title": "給一年後的自己",
            "content": "堅持熱愛，奔赴山海！"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Letter updated successfully.",
                "zh": "信件更新成功。"
            },
            "message_eng": "Letter updated successfully.",
            "message_chinese": "信件更新成功。",
            "data": {
                "id": 1,
                "sticker": "bear",
                "title": "未來的我，你好！",
                "content": "希望那時候的我，已經實現了現在的夢想...",
                "status": "opened",
                "status_display": {
                    "en": "Opened",
                    "zh": "已開啟"
                },
                "is_opened": true,
                "date": "2026-10-27",
                "formatted_date_zh": "2026年10月27日",
                "formatted_date_en": "October 27, 2026",
                "content_length": 34,
                "opened_at": "2026-10-27T10:20:00Z",
                "created_at": "2026-10-27T10:15:00Z",
                "updated_at": "2026-10-27T10:38:00Z"
            }
        }
        ```

        **Response Body - 400 Bad Request (Invalid Status) (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "status: \"invalid\" is not a valid choice.",
                "zh": "状态: \"invalid\" 不是有效选项。"
            },
            "message_eng": "status: \"invalid\" is not a valid choice.",
            "message_chinese": "状态: \"invalid\" 不是有效选项。"
        }
        ```

        **Response Body - 404 Not Found (JSON):**
        ```json
        {
            "success": false,
            "status_code": 404,
            "message": {
                "en": "Letter not found.",
                "zh": "未找到该信件。"
            },
            "message_eng": "Letter not found.",
            "message_chinese": "未找到该信件。"
        }
        ```
        """
        return self._update_letter(request, pk, partial=True)

    def _update_letter(self, request, pk, partial=False):
        letter = self._get_letter(request, pk)
        if not letter:
            return self.error_response(
                "Letter not found.",
                "未找到该信件。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(letter, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if 'sticker' in serializer.validated_data:
            letter.sticker = serializer.validated_data['sticker']
        if 'title' in serializer.validated_data:
            letter.title = serializer.validated_data['title']
        if 'content' in serializer.validated_data:
            letter.content = serializer.validated_data['content']
        if 'status' in serializer.validated_data:
            new_status = serializer.validated_data['status']
            letter.status = new_status
            if new_status == LetterStatus.OPENED and not letter.opened_at:
                letter.opened_at = timezone.now()
            elif new_status == LetterStatus.PENDING:
                letter.opened_at = None
        letter.save()

        return self.success_response(
            en_msg="Letter updated successfully.",
            zh_msg="信件更新成功。",
            status_code=status.HTTP_200_OK,
            data=LetterSerializer(letter).data
        )

    @swagger_auto_schema(
        tags=['My Letters'],
        responses={
            status.HTTP_200_OK: 'Letter deleted successfully',
            status.HTTP_404_NOT_FOUND: 'Letter not found',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def delete(self, request, pk):
        """
        **Delete Letter - Authenticated Users**

        Permanently deletes an existing letter belonging to the authenticated user.
        Attempts to delete another user's letter will return `404 Not Found`.

        **Method:** `DELETE`
        **Endpoint:** `/api/v1/letters/<pk>/` (also `/api/v1/my-letters/<pk>/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Letter deleted successfully.",
                "zh": "信件已成功删除。"
            },
            "message_eng": "Letter deleted successfully.",
            "message_chinese": "信件已成功删除。"
        }
        ```

        **Response Body - 404 Not Found (JSON):**
        ```json
        {
            "success": false,
            "status_code": 404,
            "message": {
                "en": "Letter not found.",
                "zh": "未找到该信件。"
            },
            "message_eng": "Letter not found.",
            "message_chinese": "未找到该信件。"
        }
        ```
        """
        letter = self._get_letter(request, pk)
        if not letter:
            return self.error_response(
                "Letter not found.",
                "未找到该信件。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        letter.delete()
        return self.success_response(
            en_msg="Letter deleted successfully.",
            zh_msg="信件已成功删除。",
            status_code=status.HTTP_200_OK
        )

