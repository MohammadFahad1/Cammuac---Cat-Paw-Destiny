import random
import uuid
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from core.base import NewAPIView
from accounts.tasks import send_otp_email_task
from accounts.serializers import (
    UserRegistrationSerializer,
    EmailOTPSerializer,
    EmailSerializer,
    EmptySerializer,
    EmailPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
)

User = get_user_model()


def _get_user_profile_data(user, request=None):
    return {
        'id': user.id,
        'email': user.email,
        'status': user.status,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'last_login': user.last_login,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
    }


class UserRegistrationAPIView(NewAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=UserRegistrationSerializer,
        responses={
            status.HTTP_201_CREATED: EmptySerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request'
        }
    )
    def post(self, request):
        """
        **User Registration - Public**

        Endpoint for creating a new user account with email and password.
        An OTP code is generated and dispatched to the email for account activation.

        **Method:** `POST`
        **Endpoint:** `/api/v1/auth/signup/`
        **Authentication:** None (Public)

        **Request Body (JSON):**
        ```json
        {
            "email": "user@example.com",
            "password": "SecurePassword123!"
        }
        ```

        **Response Body - 201 Created (JSON):**
        ```json
        {
            "success": true,
            "status_code": 201,
            "message": {
                "en": "Registration successful. Check your email for verification code.",
                "zh": "注册成功。请查看您的电子邮件以获取验证码。"
            },
            "message_eng": "Registration successful. Check your email for verification code.",
            "message_chinese": "注册成功。请查看您的电子邮件以获取验证码。"
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "A user with this email already exists.",
                "zh": "具有此电子邮件的用户已存在。"
            },
            "message_eng": "A user with this email already exists.",
            "message_chinese": "具有此电子邮件的用户已存在。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = random.randint(100000, 999999)
        user = serializer.save(
            is_active=False,
            status=User.INACTIVE,
            otp=otp,
            otp_created_at=timezone.now()
        )

        send_otp_email_task.delay(user.email, otp, "Activation")

        return self.success_response(
            en_msg="Registration successful. Check your email for verification code.",
            zh_msg="注册成功。请查看您的电子邮件以获取验证码。",
            status_code=status.HTTP_201_CREATED
        )


class VerifyEmailOTPAPIView(NewAPIView):
    serializer_class = EmailOTPSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=EmailOTPSerializer,
        responses={
            status.HTTP_200_OK: EmptySerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request'
        }
    )
    def post(self, request):
        """
        **Email OTP Verification - Public**

        Verifies the 6-digit OTP sent to the user's email after registration
        and activates the account (`is_active=True`, `status='active'`).

        **Method:** `POST`
        **Endpoint:** `/api/v1/auth/signup/verify-email/`
        **Authentication:** None (Public)

        **Request Body (JSON):**
        ```json
        {
            "email": "user@example.com",
            "otp": "123456"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Email OTP verification successful.",
                "zh": "邮箱验证码验证成功。"
            },
            "message_eng": "Email OTP verification successful.",
            "message_chinese": "邮箱验证码验证成功。"
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "Invalid OTP.",
                "zh": "验证码无效。"
            },
            "message_eng": "Invalid OTP.",
            "message_chinese": "验证码无效。"
        }
        ```

        **Response Body - 404 Not Found (JSON):**
        ```json
        {
            "success": false,
            "status_code": 404,
            "message": {
                "en": "User not found.",
                "zh": "用户不存在。"
            },
            "message_eng": "User not found.",
            "message_chinese": "用户不存在。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'].lower().strip()
        otp = serializer.validated_data['otp']

        user = User.objects.filter(email=email).first()
        if not user:
            return self.error_response(
                "User not found.",
                "用户不存在。",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if str(user.otp) != str(otp):
            return self.error_response(
                "Invalid OTP.",
                "验证码无效。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if user.otp_created_at and user.otp_created_at < timezone.now() - timedelta(minutes=15):
            return self.error_response(
                "OTP has expired.",
                "验证码已过期。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.status = User.ACTIVE
        user.otp = None
        user.otp_created_at = None
        user.save()

        return self.success_response(
            en_msg="Email OTP verification successful.",
            zh_msg="邮箱验证码验证成功。",
            status_code=status.HTTP_200_OK
        )


class LoginAPIView(NewAPIView):
    serializer_class = EmailPasswordSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        tags=["Authentication"],
        request_body=EmailPasswordSerializer
    )
    def post(self, request, *args, **kwargs):
        """
        **User Login - Public**

        Authenticates user with email and password, returning JWT access and refresh tokens.

        **Method:** `POST`
        **Endpoint:** `/api/v1/auth/login/`
        **Authentication:** None (Public)

        **Request Body (JSON):**
        ```json
        {
            "email": "user@example.com",
            "password": "SecurePassword123!"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Login successful.",
                "zh": "登录成功。"
            },
            "message_eng": "Login successful.",
            "message_chinese": "登录成功。",
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "user": {
                "id": 1,
                "email": "user@example.com",
                "status": "active",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false,
                "last_login": "2026-10-26T16:00:00Z",
                "created_at": "2026-10-26T15:00:00Z",
                "updated_at": "2026-10-26T16:00:00Z"
            }
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "Invalid password.",
                "zh": "密码错误。"
            },
            "message_eng": "Invalid password.",
            "message_chinese": "密码错误。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email").lower().strip()
        password = serializer.validated_data.get("password")

        user = User.objects.filter(email=email).first()
        if not user:
            return self.error_response(
                "User does not exist.",
                "用户不存在。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(password):
            return self.error_response(
                "Invalid password.",
                "密码错误。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if user.status == User.BLOCKED:
            return self.error_response(
                "User account is blocked.",
                "用户账户已被封禁。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_active or user.status != User.ACTIVE:
            return self.error_response(
                "User account is not activated.",
                "用户账户未激活。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return self.success_response(
            en_msg="Login successful.",
            zh_msg="登录成功。",
            status_code=status.HTTP_200_OK,
            access=str(access),
            refresh=str(refresh),
            user=_get_user_profile_data(user, request)
        )


class ForgotPasswordAPIView(NewAPIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=EmailSerializer
    )
    def post(self, request):
        """
        **Forgot Password - Public**

        Initiates password reset process by generating a 6-digit OTP code
        and dispatching it to the user's registered email address.

        **Method:** `POST`
        **Endpoint:** `/api/v1/auth/forgot-password/`
        **Authentication:** None (Public)

        **Request Body (JSON):**
        ```json
        {
            "email": "user@example.com"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "An OTP has been sent to your email. Please check your inbox to reset your password.",
                "zh": "验证码已发送至您的邮箱，请检查收件箱以重置密码。"
            },
            "message_eng": "An OTP has been sent to your email. Please check your inbox to reset your password.",
            "message_chinese": "验证码已发送至您的邮箱，请检查收件箱以重置密码。"
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "User not found.",
                "zh": "用户不存在。"
            },
            "message_eng": "User not found.",
            "message_chinese": "用户不存在。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email').lower().strip()
        user = User.objects.filter(email=email).first()
        if not user:
            return self.error_response(
                "User not found.",
                "用户不存在。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if user.otp_created_at and (timezone.now() - user.otp_created_at) < timedelta(minutes=1):
            return self.error_response(
                "An OTP has already been sent to your email. Please try again in 1 minute.",
                "验证码已发送至您的邮箱，请在 1 分钟后重试。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        otp = str(random.randint(100000, 999999))
        reset_token = str(uuid.uuid4())
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.forgot_password_token = reset_token
        user.save()

        send_otp_email_task.delay(email, otp, "Password Reset")

        return self.success_response(
            en_msg="An OTP has been sent to your email. Please check your inbox to reset your password.",
            zh_msg="验证码已发送至您的邮箱，请检查收件箱以重置密码。",
            status_code=status.HTTP_200_OK
        )


class ForgotPasswordVerifyOTPAPIView(NewAPIView):
    serializer_class = EmailOTPSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=EmailOTPSerializer
    )
    def post(self, request):
        """
        **Forgot Password Verify OTP - Public**

        Verifies the OTP sent for password reset and returns a temporary `reset_token` (UUID)
        required for setting the new password.

        **Method:** `POST`
        **Endpoint:** `/api/v1/auth/forgot-password/verify-otp/`
        **Authentication:** None (Public)

        **Request Body (JSON):**
        ```json
        {
            "email": "user@example.com",
            "otp": "123456"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "OTP verified successfully.",
                "zh": "验证码验证成功。"
            },
            "message_eng": "OTP verified successfully.",
            "message_chinese": "验证码验证成功。",
            "email": "user@example.com",
            "reset_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "Invalid OTP.",
                "zh": "验证码无效。"
            },
            "message_eng": "Invalid OTP.",
            "message_chinese": "验证码无效。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email').lower().strip()
        otp = serializer.validated_data.get('otp')

        user = User.objects.filter(email=email).first()
        if not user:
            return self.error_response(
                "User not found.",
                "用户不存在。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if str(user.otp) != str(otp):
            return self.error_response(
                "Invalid OTP.",
                "验证码无效。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not user.otp_created_at or (timezone.now() - user.otp_created_at) > timedelta(minutes=15):
            user.forgot_password_token = None
            user.otp = None
            user.otp_created_at = None
            user.save()
            return self.error_response(
                "OTP has expired. Please initiate the forgot password process again.",
                "验证码已过期，请重新发起找回密码流程。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user.otp = None
        user.otp_created_at = None
        user.save()

        return self.success_response(
            en_msg="OTP verified successfully.",
            zh_msg="验证码验证成功。",
            status_code=status.HTTP_200_OK,
            email=email,
            reset_token=str(user.forgot_password_token)
        )

class ResetPasswordAPIView(NewAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=ResetPasswordSerializer
    )
    def post(self, request):
        """
        **Reset Password - Public**

        Resets user password using the `reset_token` obtained from OTP verification.

        **Method:** `POST`
        **Endpoint:** `/api/v1/auth/reset-password/`
        **Authentication:** None (Public)

        **Request Body (JSON):**
        ```json
        {
            "email": "user@example.com",
            "reset_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "new_password": "NewSecurePassword123!"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Password reset successfully.",
                "zh": "密码重置成功。"
            },
            "message_eng": "Password reset successfully.",
            "message_chinese": "密码重置成功。"
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "Invalid reset token.",
                "zh": "重置令牌无效。"
            },
            "message_eng": "Invalid reset token.",
            "message_chinese": "重置令牌无效。"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email').lower().strip()
        reset_token = serializer.validated_data.get('reset_token')
        new_password = serializer.validated_data.get('new_password')

        user = User.objects.filter(email=email).first()
        if not user:
            return self.error_response(
                "User not found.",
                "用户不存在。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not user.forgot_password_token or str(user.forgot_password_token) != str(reset_token):
            return self.error_response(
                "Invalid reset token.",
                "重置令牌无效。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user=user)
        except Exception as e:
            from core.messages import extract_bilingual_errors
            bilingual = extract_bilingual_errors(str(e))
            return self.error_response(
                en_msg=bilingual['en'],
                zh_msg=bilingual['zh'],
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.forgot_password_token = None
        user.otp = None
        user.otp_created_at = None
        user.save()

        return self.success_response(
            en_msg="Password reset successfully.",
            zh_msg="密码重置成功。",
            status_code=status.HTTP_200_OK
        )


class ChangePasswordAPIView(NewAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=ChangePasswordSerializer
    )
    def post(self, request):
        """
        **Change Password - Authenticated Users**

        Allows an authenticated user to change their password by validating old password
        and setting a new password.

        **Method:** `POST`
        **Endpoint:** `/api/v1/auth/change-password/`
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body (JSON):**
        ```json
        {
            "old_password": "CurrentPassword123!",
            "new_password": "NewSecurePassword123!"
        }
        ```

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "Password changed successfully.",
                "zh": "密码修改成功。"
            },
            "message_eng": "Password changed successfully.",
            "message_chinese": "密码修改成功。"
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "Incorrect old password.",
                "zh": "原密码不正确。"
            },
            "message_eng": "Incorrect old password.",
            "message_chinese": "原密码不正确。"
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        user = request.user
        if not user.check_password(old_password):
            return self.error_response(
                "Incorrect old password.",
                "原密码不正确。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if old_password == new_password:
            return self.error_response(
                "New password cannot be the same as old password.",
                "新密码不能与原密码相同。",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user=user)
        except Exception as e:
            from core.messages import extract_bilingual_errors
            bilingual = extract_bilingual_errors(str(e))
            return self.error_response(
                en_msg=bilingual['en'],
                zh_msg=bilingual['zh'],
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return self.success_response(
            en_msg="Password changed successfully.",
            zh_msg="密码修改成功。",
            status_code=status.HTTP_200_OK
        )


class UserProfileAPIView(NewAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    @swagger_auto_schema(
        tags=['Authentication'],
        responses={
            status.HTTP_200_OK: UserProfileSerializer,
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, request):
        """
        **User Profile - Authenticated Users (Read-Only)**

        Retrieves profile information for the authenticated user.
        Note: Profile updating is not permitted on this API.

        **Method:** `GET`
        **Endpoint:** `/api/v1/auth/profile/`
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "User profile retrieved successfully.",
                "zh": "成功获取用户个人信息。"
            },
            "message_eng": "User profile retrieved successfully.",
            "message_chinese": "成功获取用户个人信息。",
            "data": {
                "id": 1,
                "email": "user@example.com",
                "status": "active",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false,
                "last_login": "2026-10-26T16:00:00Z",
                "created_at": "2026-10-26T15:00:00Z",
                "updated_at": "2026-10-26T16:00:00Z"
            }
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
        user = request.user
        profile_data = _get_user_profile_data(user, request)
        return self.success_response(
            en_msg="User profile retrieved successfully.",
            zh_msg="成功获取用户个人信息。",
            status_code=status.HTTP_200_OK,
            data=profile_data
        )


class DeleteUserAccountAPIView(NewAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    @swagger_auto_schema(tags=['Authentication'])
    def delete(self, request):
        """
        **Delete User Account - Authenticated Users**

        Permanently deletes the authenticated user's account.
        Superuser accounts cannot be deleted through this endpoint.

        **Method:** `DELETE`
        **Endpoint:** `/api/v1/auth/delete-account/`
        **Authentication:** JWT Bearer Token (`IsAuthenticated`)
        **Headers:** `Authorization: Bearer <access_token>`

        **Request Body:** None

        **Response Body - 200 OK (JSON):**
        ```json
        {
            "success": true,
            "status_code": 200,
            "message": {
                "en": "User account deleted successfully.",
                "zh": "用户账户已成功删除。"
            },
            "message_eng": "User account deleted successfully.",
            "message_chinese": "用户账户已成功删除。"
        }
        ```

        **Response Body - 400 Bad Request (JSON):**
        ```json
        {
            "success": false,
            "status_code": 400,
            "message": {
                "en": "Superuser account cannot be deleted.",
                "zh": "超级用户账户不能删除。"
            },
            "message_eng": "Superuser account cannot be deleted.",
            "message_chinese": "超级用户账户不能删除。"
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
        user = request.user
        if user.is_superuser:
            return self.error_response(
                "Superuser account cannot be deleted.",
                "超级用户账户不能删除。",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user.delete()
        return self.success_response(
            en_msg="User account deleted successfully.",
            zh_msg="用户账户已成功删除。",
            status_code=status.HTTP_200_OK
        )

