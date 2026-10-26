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
