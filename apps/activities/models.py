from django.db import models
from django.conf import settings
from django.utils import timezone


class DailyCheckIn(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_check_ins'
    )
    date = models.DateField(default=timezone.localdate, db_index=True)
    good_for = models.JSONField(help_text="Items favorable for today (bilingual)")
    avoid = models.JSONField(help_text="Items to avoid for today (bilingual)")
    quote = models.JSONField(help_text="Daily inspirational quote (bilingual)")
    lucky_color = models.JSONField(help_text="Lucky color (bilingual and hex)")
    lucky_number = models.PositiveIntegerField(help_text="Lucky number")
    lucky_direction = models.JSONField(help_text="Lucky direction (bilingual)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Daily Check-in'
        verbose_name_plural = 'Daily Check-ins'
        unique_together = ('user', 'date')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.date}"


# Backwards compatibility alias
DailyActivity = DailyCheckIn


class Alarm(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='alarms'
    )
    time = models.CharField(
        max_length=10,
        help_text="Alarm time in HH:MM format (e.g., '04:30')"
    )
    period = models.CharField(
        max_length=5,
        choices=[('AM', 'AM'), ('PM', 'PM')],
        default='AM',
        help_text="Period (AM or PM)"
    )
    title_zh = models.CharField(
        max_length=100,
        help_text="Alarm title in Chinese (e.g., '起床囉！')"
    )
    title_en = models.CharField(
        max_length=100,
        help_text="Alarm title in English (e.g., 'Wake Up!')"
    )
    repeat = models.CharField(
        max_length=100,
        default="每天 Every day",
        help_text="Repeat pattern (e.g., '每天 Every day')"
    )
    icon_emoji = models.CharField(
        max_length=50,
        default="🌅🐱",
        help_text="Icon and emoji (e.g., '🌅🐱')"
    )
    bg_color = models.CharField(
        max_length=50,
        default="bg-pink-50",
        help_text="Background Tailwind color class (e.g., 'bg-pink-50')"
    )
    border_color = models.CharField(
        max_length=50,
        default="border-pink-200",
        help_text="Border Tailwind color class (e.g., 'border-pink-200')"
    )
    enabled = models.BooleanField(
        default=True,
        help_text="Whether the alarm is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Alarm'
        verbose_name_plural = 'Alarms'
        ordering = ['id']

    def __str__(self):
        return f"{self.user.email} - {self.time} {self.period} ({self.title_en})"

