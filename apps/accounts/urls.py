from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.UserRegistrationAPIView.as_view(), name='signup'),
    path('signup/verify-email/', views.VerifyEmailOTPAPIView.as_view(), name='signup-verify-email'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('google/', views.GoogleSignInAPIView.as_view(), name='google-login'),
    path('forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('forgot-password/verify-otp/', views.ForgotPasswordVerifyOTPAPIView.as_view(), name='forgot-password-verify-otp'),
    path('reset-password/', views.ResetPasswordAPIView.as_view(), name='reset-password'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
    path('profile/', views.UserProfileAPIView.as_view(), name='user-profile'),
    path('delete-account/', views.DeleteUserAccountAPIView.as_view(), name='delete-user-account'),
]
