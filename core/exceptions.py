import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from core.messages import extract_bilingual_errors

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework.
    Formats error responses in both English and Chinese:
    {
        "success": false,
        "status_code": 400,
        "message": {
            "en": "error message",
            "zh": "中文错误信息"
        },
        "message_eng": "error message",
        "message_chinese": "中文错误信息"
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        message_dict = extract_bilingual_errors(response.data)
        response.data = {
            "success": False,
            "status_code": response.status_code,
            "message": message_dict,
            "message_eng": message_dict["en"],
            "message_chinese": message_dict["zh"],
        }
        return response

    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return Response({
        "success": False,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": {
            "en": "Internal server error.",
            "zh": "服务器内部错误。"
        },
        "message_eng": "Internal server error.",
        "message_chinese": "服务器内部错误。",
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
