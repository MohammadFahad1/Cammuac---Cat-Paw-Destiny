from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from django.utils import timezone

@shared_task
def send_otp_email_task(email, otp, purpose="Activation"):
    """
    Celery task to send account verification OTP via HTML email template (bilingual).
    """
    if purpose == "Activation":
        subject = "Paw - 账户验证码 / Verification Code"
        purpose_zh = "注册激活"
    elif purpose == "Password Reset":
        subject = "Paw - 重置密码验证码 / Password Reset Code"
        purpose_zh = "重置密码"
    else:
        subject = f"Paw - {purpose} 验证码 / Verification Code"
        purpose_zh = purpose

    raw_from = (
        getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        or getattr(settings, 'EMAIL_HOST_USER', None)
        or 'noreply@paw.app'
    )
    from_email = f"Paw <{raw_from}>" if raw_from and '<' not in raw_from else (raw_from or 'Paw <noreply@paw.app>')

    context = {
        'otp': otp,
        'purpose': purpose,
        'purpose_zh': purpose_zh,
        'email': email,
        'current_year': timezone.now().year,
    }

    html_message = render_to_string('otp_template.html', context)
    plain_message = (
        f"【Paw】您的验证码是：{otp}（15分钟内有效，请勿泄露给他人）。\n"
        f"Your Paw verification code is: {otp} (valid for 15 minutes, do not share with anyone)."
    )

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=True,
    )
