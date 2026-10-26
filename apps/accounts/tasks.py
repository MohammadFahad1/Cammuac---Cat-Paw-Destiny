from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from django.utils import timezone

@shared_task
def send_otp_email_task(email, otp, purpose="Activation"):
    """
    Celery task to send account verification OTP via HTML email template.
    """
    subject = f"Cammuac - Cat Paw Destiny - {purpose} Verification Code"
    from_email = (
        getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        or getattr(settings, 'EMAIL_HOST_USER', None)
        or 'noreply@cammuac.com'
    )

    context = {
        'otp': otp,
        'purpose': purpose,
        'email': email,
        'current_year': timezone.now().year,
    }

    html_message = render_to_string('otp_template.html', context)
    plain_message = f"Your Cammuac - Cat Paw Destiny verification code is {otp}. It is valid for 15 minutes."

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=True,
    )
