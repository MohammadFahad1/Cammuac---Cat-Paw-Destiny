from django.db import models
from django.conf import settings
from django.utils import timezone


class DiaryNote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diary_notes'
    )
    icon = models.CharField(
        max_length=100,
        help_text="Icon identifier, name, or emoji representing the mood/entry"
    )
    date = models.DateField(
        default=timezone.localdate,
        db_index=True,
        help_text="Date of the diary note"
    )
    note = models.TextField(
        help_text="Text content of the diary note"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Diary Note'
        verbose_name_plural = 'Diary Notes'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.date} ({self.icon})"

