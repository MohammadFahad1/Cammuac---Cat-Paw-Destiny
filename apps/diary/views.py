from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from core.base import NewAPIView
from .models import DiaryNote
from .serializers import DiaryNoteSerializer, DiaryNoteCreateSerializer


class DiaryNoteListCreateAPIView(NewAPIView):
    serializer_class = DiaryNoteCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        tags=['My Diary (Calendar)'],
        responses={
            status.HTTP_200_OK: DiaryNoteSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request):
        """
        **List All Diary Notes - Authenticated Users**

        Retrieves all diary notes created by the authenticated user without pagination.
        Notes are ordered chronologically by date and creation time descending.

        **Method:** `GET`
        **Endpoint:** `/api/v1/diary/` (also `/api/v1/my-diary/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Diary notes retrieved successfully.",
                "zh": "成功获取日记列表。"
            },
            "message_eng": "Diary notes retrieved successfully.",
            "message_chinese": "成功获取日记列表。",
            "count": 2,
            "data": [
                {
                    "id": 1,
                    "icon": "happy_cat",
                    "date": "2026-10-27",
                    "note": "Had a wonderful morning walk with my cat today!",
                    "day": 27,
                    "month_year": "Oct 2026",
                    "weekday_en": "Tue",
                    "weekday_zh": "星期二",
                    "created_at": "2026-10-27T08:30:00Z",
                    "updated_at": "2026-10-27T08:30:00Z"
                },
                {
                    "id": 2,
                    "icon": "paw_print",
                    "date": "2026-10-26",
                    "note": "Learned something new about feline nutrition.",
                    "day": 26,
                    "month_year": "Oct 2026",
                    "weekday_en": "Mon",
                    "weekday_zh": "星期一",
                    "created_at": "2026-10-26T19:15:00Z",
                    "updated_at": "2026-10-26T19:15:00Z"
                }
            ]
        }
        ```

        **Response Body - 401 Unauthorized (JSON):**
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
        notes = DiaryNote.objects.filter(user=request.user).order_by('-date', '-created_at')
        serialized_data = DiaryNoteSerializer(notes, many=True).data

        return self.success_response(
            en_msg="Diary notes retrieved successfully.",
            zh_msg="成功获取日记列表。",
            status_code=status.HTTP_200_OK,
            count=len(serialized_data),
            data=serialized_data
        )

    @swagger_auto_schema(
        tags=['My Diary (Calendar)'],
        request_body=DiaryNoteCreateSerializer,
        responses={
            status.HTTP_201_CREATED: DiaryNoteSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def post(self, request):
        """
        **Create Diary Note - Authenticated Users**

        Creates a new diary entry with an icon, a date, and a text note.

        **Method:** `POST`
        **Endpoint:** `/api/v1/diary/` (also `/api/v1/my-diary/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body (JSON):**
        ```json
        {
            "icon": "happy_cat",
            "date": "2026-10-27",
            "note": "Had a peaceful and productive day with lots of smiles."
        }
        ```

        **Response Body - 201 Created (JSON):**
        ```json
        {
            "success": true,
            "status_code": 201,
            "message": {
                "en": "Diary note created successfully.",
                "zh": "日记创建成功。"
            },
            "message_eng": "Diary note created successfully.",
            "message_chinese": "日记创建成功。",
            "data": {
                "id": 1,
                "icon": "happy_cat",
                "date": "2026-10-27",
                "note": "Had a peaceful and productive day with lots of smiles.",
                "day": 27,
                "month_year": "Oct 2026",
                "weekday_en": "Tue",
                "weekday_zh": "星期二",
                "created_at": "2026-10-27T09:00:00Z",
                "updated_at": "2026-10-27T09:00:00Z"
            }
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "icon: This field is required.; date: This field is required.",
                "zh": "图标: 此字段为必填项。; 日期: 此字段为必填项。"
            },
            "message_eng": "icon: This field is required.; date: This field is required.",
            "message_chinese": "图标: 此字段为必填项。; 日期: 此字段为必填项。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note_instance = DiaryNote.objects.create(
            user=request.user,
            icon=serializer.validated_data['icon'],
            date=serializer.validated_data['date'],
            note=serializer.validated_data['note']
        )

        return self.success_response(
            en_msg="Diary note created successfully.",
            zh_msg="日记创建成功。",
            status_code=status.HTTP_201_CREATED,
            data=DiaryNoteSerializer(note_instance).data
        )


class DiaryNoteDetailAPIView(NewAPIView):
    serializer_class = DiaryNoteCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def _get_note(self, request, pk):
        return DiaryNote.objects.filter(pk=pk, user=request.user).first()

    @swagger_auto_schema(
        tags=['My Diary (Calendar)'],
        responses={
            status.HTTP_200_OK: DiaryNoteSerializer,
            status.HTTP_404_NOT_FOUND: 'Diary note not found',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request, pk):
        """
        **Get Specific Diary Note Details - Authenticated Users**

        Retrieves the complete details of a specific diary note by its ID.
        Only notes owned by the authenticated user can be accessed.

        **Method:** `GET`
        **Endpoint:** `/api/v1/diary/<pk>/` (also `/api/v1/my-diary/<pk>/`)
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Diary note details retrieved successfully.",
                "zh": "成功获取日记详情。"
            },
            "message_eng": "Diary note details retrieved successfully.",
            "message_chinese": "成功获取日记详情。",
            "data": {
                "id": 1,
                "icon": "happy_cat",
                "date": "2026-10-27",
                "note": "Had a wonderful morning walk with my cat today!",
                "day": 27,
                "month_year": "Oct 2026",
                "weekday_en": "Tue",
                "weekday_zh": "星期二",
                "created_at": "2026-10-27T08:30:00Z",
                "updated_at": "2026-10-27T08:30:00Z"
            }
        }
        ```

        **Response Body - 404 Not Found (JSON):**
        ```json
        {
            "success": false,
            "status_code": 404,
            "message": {
                "en": "Diary note not found.",
                "zh": "未找到该日记。"
            },
            "message_eng": "Diary note not found.",
            "message_chinese": "未找到该日记。"
        }
        ```
        """
        note = self._get_note(request, pk)
        if not note:
            return self.error_response(
                "Diary note not found.",
                "未找到该日记。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.success_response(
            en_msg="Diary note details retrieved successfully.",
            zh_msg="成功获取日记详情。",
            status_code=status.HTTP_200_OK,
            data=DiaryNoteSerializer(note).data
        )

    @swagger_auto_schema(
        tags=['My Diary (Calendar)'],
        request_body=DiaryNoteCreateSerializer,
        responses={
            status.HTTP_200_OK: DiaryNoteSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Diary note not found'
        }
    )
    def put(self, request, pk):
        """
        **Update Specific Diary Note - Authenticated Users**

        Updates the icon, date, and/or text note of an existing diary entry.

        **Method:** `PUT`
        **Endpoint:** `/api/v1/diary/<pk>/`
        """
        note = self._get_note(request, pk)
        if not note:
            return self.error_response(
                "Diary note not found.",
                "未找到该日记。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(note, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'icon' in serializer.validated_data:
            note.icon = serializer.validated_data['icon']
        if 'date' in serializer.validated_data:
            note.date = serializer.validated_data['date']
        if 'note' in serializer.validated_data:
            note.note = serializer.validated_data['note']
        note.save()

        return self.success_response(
            en_msg="Diary note updated successfully.",
            zh_msg="日记更新成功。",
            status_code=status.HTTP_200_OK,
            data=DiaryNoteSerializer(note).data
        )

    @swagger_auto_schema(
        tags=['My Diary (Calendar)'],
        responses={
            status.HTTP_200_OK: 'Diary note deleted successfully',
            status.HTTP_404_NOT_FOUND: 'Diary note not found'
        }
    )
    def delete(self, request, pk):
        """
        **Delete Specific Diary Note - Authenticated Users**

        Deletes an existing diary entry belonging to the authenticated user.

        **Method:** `DELETE`
        **Endpoint:** `/api/v1/diary/<pk>/`
        """
        note = self._get_note(request, pk)
        if not note:
            return self.error_response(
                "Diary note not found.",
                "未找到该日记。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        note.delete()
        return self.success_response(
            en_msg="Diary note deleted successfully.",
            zh_msg="日记已成功删除。",
            status_code=status.HTTP_200_OK
        )

