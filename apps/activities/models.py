from django.db import models
from django.conf import settings
from django.utils import timezone


class DayStatusType(models.TextChoices):
    LUCKY = 'lucky', 'Lucky (大吉)'
    BAD_LUCK = 'bad_luck', 'Bad Luck (凶)'
    NORMAL = 'normal', 'Normal (平)'


DAY_STATUS_MAP = {
    'lucky': {
        'code': 'lucky',
        'status': 'Lucky',
        'name_en': 'Lucky',
        'name_zh': '大吉',
        'en': 'Lucky',
        'zh': '大吉',
    },
    'bad_luck': {
        'code': 'bad_luck',
        'status': 'Bad Luck',
        'name_en': 'Bad Luck',
        'name_zh': '凶',
        'en': 'Bad Luck',
        'zh': '凶',
    },
    'normal': {
        'code': 'normal',
        'status': 'Normal',
        'name_en': 'Normal',
        'name_zh': '平',
        'en': 'Normal',
        'zh': '平',
    },
}


def get_day_status_payload(status_key: str) -> dict:
    if not status_key:
        return DAY_STATUS_MAP['normal']
    key = str(status_key).lower().strip().replace(' ', '_').replace('-', '_')
    if key in ('good', 'lucky'):
        return DAY_STATUS_MAP['lucky']
    if key in ('bad', 'bad_luck', 'bad_luch'):
        return DAY_STATUS_MAP['bad_luck']
    return DAY_STATUS_MAP.get(key, DAY_STATUS_MAP['normal'])


class DayStatus(models.Model):
    date = models.DateField(
        unique=True,
        db_index=True,
        help_text="Calendar date for the day status (entered manually in admin)"
    )
    status = models.CharField(
        max_length=20,
        choices=DayStatusType.choices,
        default=DayStatusType.NORMAL,
        help_text="Status for this date: Lucky (大吉), Bad Luck (凶), or Normal (平)"
    )
    note = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Optional note for admin reference"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Day Status'
        verbose_name_plural = 'Day Statuses'
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.get_status_display()}"


class DailyCheckIn(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_check_ins'
    )
    date = models.DateField(default=timezone.localdate, db_index=True)
    day_status = models.CharField(
        max_length=20,
        default=DayStatusType.NORMAL,
        blank=True,
        help_text="Day status snapshot: lucky, bad_luck, or normal"
    )
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

