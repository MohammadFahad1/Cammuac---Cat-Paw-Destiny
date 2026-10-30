from datetime import timedelta
from unittest.mock import patch
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "StrongPass123!@#"
        self.signup_url = "/api/v1/auth/signup/"
        self.verify_otp_url = "/api/v1/auth/signup/verify-email/"
        self.login_url = "/api/v1/auth/login/"
        self.forgot_password_url = "/api/v1/auth/forgot-password/"
        self.forgot_verify_otp_url = "/api/v1/auth/forgot-password/verify-otp/"
        self.reset_password_url = "/api/v1/auth/reset-password/"
        self.change_password_url = "/api/v1/auth/change-password/"
        self.profile_url = "/api/v1/auth/profile/"
        self.delete_account_url = "/api/v1/auth/delete-account/"

    @patch("accounts.tasks.send_otp_email_task.delay")
    def test_signup_success(self, mock_send_email):
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertIn("en", response.data["message"])
        self.assertIn("zh", response.data["message"])
        self.assertEqual(response.data["message"]["en"], "Registration successful. Check your email for verification code.")
        self.assertEqual(response.data["message"]["zh"], "注册成功。请查看您的电子邮件以获取验证码。")
        self.assertEqual(response.data["message_eng"], "Registration successful. Check your email for verification code.")
        self.assertEqual(response.data["message_chinese"], "注册成功。请查看您的电子邮件以获取验证码。")

        user = User.objects.filter(email=self.email).first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active)
        self.assertEqual(user.status, User.INACTIVE)
        self.assertIsNotNone(user.otp)
        mock_send_email.assert_called_once()

    def test_signup_validation_error_bilingual(self):
        # Missing password
        data = {"email": "invalid-email"}
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("en", response.data["message"])
        self.assertIn("zh", response.data["message"])
        self.assertIn("password", response.data["message"]["en"])
        self.assertIn("密码", response.data["message"]["zh"])

    def test_patient_signup_endpoint_removed(self):
        response = self.client.post("/api/v1/auth/patient/signup/", {"email": self.email, "password": self.password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_verify_email_otp(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=False,
            status=User.INACTIVE,
            otp=123456,
            otp_created_at=timezone.now()
        )

        # Invalid OTP
        res_invalid = self.client.post(self.verify_otp_url, {"email": self.email, "otp": "999999"}, format="json")
        self.assertEqual(res_invalid.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_invalid.data["message"]["en"], "Invalid OTP.")
        self.assertEqual(res_invalid.data["message"]["zh"], "验证码无效。")

        # Expired OTP
        user.otp_created_at = timezone.now() - timedelta(minutes=20)
        user.save()
        res_expired = self.client.post(self.verify_otp_url, {"email": self.email, "otp": "123456"}, format="json")
        self.assertEqual(res_expired.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_expired.data["message"]["en"], "OTP has expired.")
        self.assertEqual(res_expired.data["message"]["zh"], "验证码已过期。")

        # Correct OTP
        user.otp_created_at = timezone.now()
        user.save()
        res_valid = self.client.post(self.verify_otp_url, {"email": self.email, "otp": "123456"}, format="json")
        self.assertEqual(res_valid.status_code, status.HTTP_200_OK)
        self.assertTrue(res_valid.data["success"])
        self.assertEqual(res_valid.data["message"]["en"], "Email OTP verification successful.")
        self.assertEqual(res_valid.data["message"]["zh"], "邮箱验证码验证成功。")

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(user.status, User.ACTIVE)
        self.assertIsNone(user.otp)

    def test_verify_email_otp_bypass_code_111111(self):
        user = User.objects.create_user(
            email="bypass_user@example.com",
            password="Password123!",
            is_active=False,
            status=User.INACTIVE,
            otp=654321,
            otp_created_at=timezone.now()
        )

        # Using hardcoded test bypass code 111111
        res_bypass = self.client.post(self.verify_otp_url, {"email": user.email, "otp": "111111"}, format="json")
        self.assertEqual(res_bypass.status_code, status.HTTP_200_OK)
        self.assertTrue(res_bypass.data["success"])
        self.assertEqual(res_bypass.data["message"]["en"], "Email OTP verification successful.")

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(user.status, User.ACTIVE)
        self.assertIsNone(user.otp)

    def test_login_flow(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=True,
            status=User.ACTIVE
        )

        # Wrong password
        res_wrong_pw = self.client.post(self.login_url, {"email": self.email, "password": "wrong"}, format="json")
        self.assertEqual(res_wrong_pw.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_wrong_pw.data["message"]["en"], "Invalid password.")
        self.assertEqual(res_wrong_pw.data["message"]["zh"], "密码错误。")

        # Inactive user
        user.is_active = False
        user.status = User.INACTIVE
        user.save()
        res_inactive = self.client.post(self.login_url, {"email": self.email, "password": self.password}, format="json")
        self.assertEqual(res_inactive.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_inactive.data["message"]["en"], "User account is not activated.")
        self.assertEqual(res_inactive.data["message"]["zh"], "用户账户未激活。")

        # Blocked user
        user.is_active = True
        user.status = User.BLOCKED
        user.save()
        res_blocked = self.client.post(self.login_url, {"email": self.email, "password": self.password}, format="json")
        self.assertEqual(res_blocked.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_blocked.data["message"]["en"], "User account is blocked.")
        self.assertEqual(res_blocked.data["message"]["zh"], "用户账户已被封禁。")

        # Success login
        user.status = User.ACTIVE
        user.save()
        res_success = self.client.post(self.login_url, {"email": self.email, "password": self.password}, format="json")
        self.assertEqual(res_success.status_code, status.HTTP_200_OK)
        self.assertIn("access", res_success.data)
        self.assertIn("refresh", res_success.data)
        self.assertEqual(res_success.data["user"]["email"], self.email)
        self.assertNotIn("age", res_success.data["user"])
        self.assertNotIn("full_name", res_success.data["user"])

    @patch("accounts.tasks.send_otp_email_task.delay")
    def test_forgot_password_and_reset_flow(self, mock_send_email):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=True,
            status=User.ACTIVE
        )

        # Request OTP
        res_forgot = self.client.post(self.forgot_password_url, {"email": self.email}, format="json")
        self.assertEqual(res_forgot.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertIsNotNone(user.otp)
        otp = str(user.otp)

        # Verify OTP
        res_verify = self.client.post(self.forgot_verify_otp_url, {"email": self.email, "otp": otp}, format="json")
        self.assertEqual(res_verify.status_code, status.HTTP_200_OK)
        reset_token = res_verify.data["reset_token"]

        # Reset password
        new_password = "NewStrongPassword123!@#"
        res_reset = self.client.post(self.reset_password_url, {
            "email": self.email,
            "reset_token": reset_token,
            "new_password": new_password
        }, format="json")
        self.assertEqual(res_reset.status_code, status.HTTP_200_OK)
        self.assertEqual(res_reset.data["message"]["en"], "Password reset successfully.")
        self.assertEqual(res_reset.data["message"]["zh"], "密码重置成功。")

        # Verify login with new password
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))

    @patch("accounts.tasks.send_otp_email_task.delay")
    def test_forgot_password_verify_otp_bypass_code_111111(self, mock_send_email):
        user = User.objects.create_user(
            email="forgot_bypass@example.com",
            password="OldPassword123!",
            is_active=True,
            status=User.ACTIVE
        )

        self.client.post(self.forgot_password_url, {"email": user.email}, format="json")
        user.refresh_from_db()
        self.assertNotEqual(str(user.otp), "111111")

        # Verify using bypass code 111111
        res_verify = self.client.post(self.forgot_verify_otp_url, {"email": user.email, "otp": "111111"}, format="json")
        self.assertEqual(res_verify.status_code, status.HTTP_200_OK)
        self.assertIn("reset_token", res_verify.data)

        # Ensure reset_token can reset password
        new_pwd = "BrandNewPassword123!@#"
        res_reset = self.client.post(self.reset_password_url, {
            "email": user.email,
            "reset_token": res_verify.data["reset_token"],
            "new_password": new_pwd
        }, format="json")
        self.assertEqual(res_reset.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_pwd))

    def test_change_password(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Incorrect old password
        res_wrong = self.client.post(self.change_password_url, {
            "old_password": "WrongPassword123!",
            "new_password": "AnotherNewPassword123!@#"
        }, format="json")
        self.assertEqual(res_wrong.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_wrong.data["message"]["en"], "Incorrect old password.")
        self.assertEqual(res_wrong.data["message"]["zh"], "原密码不正确。")

        # Same password
        res_same = self.client.post(self.change_password_url, {
            "old_password": self.password,
            "new_password": self.password
        }, format="json")
        self.assertEqual(res_same.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_same.data["message"]["en"], "New password cannot be the same as old password.")
        self.assertEqual(res_same.data["message"]["zh"], "新密码不能与原密码相同。")

        # Success
        new_pw = "NewChangedPass123!@#"
        res_ok = self.client.post(self.change_password_url, {
            "old_password": self.password,
            "new_password": new_pw
        }, format="json")
        self.assertEqual(res_ok.status_code, status.HTTP_200_OK)
        self.assertEqual(res_ok.data["message"]["en"], "Password changed successfully.")
        self.assertEqual(res_ok.data["message"]["zh"], "密码修改成功。")

    def test_profile_read_only_and_put_not_allowed(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # GET profile works
        res_get = self.client.get(self.profile_url)
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(res_get.data["data"]["email"], self.email)
        self.assertEqual(res_get.data["message_eng"], "User profile retrieved successfully.")
        self.assertEqual(res_get.data["message_chinese"], "成功获取用户个人信息。")
        self.assertNotIn("age", res_get.data["data"])
        self.assertNotIn("full_name", res_get.data["data"])

        # PUT profile is NOT allowed (no profile update API)
        res_put = self.client.put(self.profile_url, {"email": "updated@example.com"}, format="json")
        self.assertEqual(res_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn("en", res_put.data["message"])
        self.assertIn("zh", res_put.data["message"])
        self.assertIn("message_eng", res_put.data)
        self.assertIn("message_chinese", res_put.data)

    def test_delete_account(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=True,
            status=User.ACTIVE
        )
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        res_delete = self.client.delete(self.delete_account_url)
        self.assertEqual(res_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(res_delete.data["message_eng"], "User account deleted successfully.")
        self.assertEqual(res_delete.data["message_chinese"], "用户账户已成功删除.") if "用户账户已成功删除." in res_delete.data["message_chinese"] else self.assertEqual(res_delete.data["message_chinese"], "用户账户已成功删除。")
        self.assertFalse(User.objects.filter(email=self.email).exists())

    @patch("core.firebase.verify_firebase_id_token")
    def test_google_login_new_user(self, mock_verify):
        mock_verify.return_value = {
            "email": "newgoogleuser@example.com",
            "email_verified": True
        }
        response = self.client.post("/api/v1/auth/google/", {"id_token": "valid_token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message_eng"], "Google login successful.")
        self.assertEqual(response.data["message_chinese"], "Google 登录成功。")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "newgoogleuser@example.com")

        user = User.objects.filter(email="newgoogleuser@example.com").first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)
        self.assertEqual(user.status, User.ACTIVE)
        self.assertFalse(user.has_usable_password())

    @patch("core.firebase.verify_firebase_id_token")
    def test_google_login_existing_user(self, mock_verify):
        User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=True,
            status=User.ACTIVE
        )
        mock_verify.return_value = {
            "email": self.email,
            "email_verified": True
        }
        response = self.client.post("/api/v1/auth/google/", {"id_token": "valid_token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message_eng"], "Google login successful.")
        self.assertEqual(response.data["message_chinese"], "Google 登录成功。")
        self.assertEqual(response.data["user"]["email"], self.email)

    @patch("core.firebase.verify_firebase_id_token")
    def test_google_login_blocked_user(self, mock_verify):
        User.objects.create_user(
            email=self.email,
            password=self.password,
            is_active=True,
            status=User.BLOCKED
        )
        mock_verify.return_value = {
            "email": self.email,
            "email_verified": True
        }
        response = self.client.post("/api/v1/auth/google/", {"id_token": "valid_token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message_eng"], "User account is blocked.")
        self.assertEqual(response.data["message_chinese"], "用户账户已被封禁。")

    @patch("core.firebase.verify_firebase_id_token")
    def test_google_login_invalid_token(self, mock_verify):
        mock_verify.side_effect = Exception("Firebase ID token verification failed")
        response = self.client.post("/api/v1/auth/google/", {"id_token": "invalid_token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message_eng"], "Invalid or expired Firebase token.")
        self.assertEqual(response.data["message_chinese"], "Firebase 令牌无效或已过期。")

    @patch("core.firebase.verify_firebase_id_token")
    def test_google_login_missing_email(self, mock_verify):
        mock_verify.return_value = {"uid": "12345"}  # No email
        response = self.client.post("/api/v1/auth/google/", {"id_token": "valid_token_no_email"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message_eng"], "Firebase ID token does not contain a valid email.")
        self.assertEqual(response.data["message_chinese"], "Firebase ID 令牌不包含有效的电子邮件。")
