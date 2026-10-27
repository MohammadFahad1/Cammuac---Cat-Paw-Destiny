from django.db import models
from django.conf import settings
from django.utils import timezone


class LetterStatus(models.TextChoices):
    PENDING = 'pending', 'Pending (待開啟)'
    OPENED = 'opened', 'Opened (已開啟)'


class Letter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='letters'
    )
    sticker = models.CharField(
        max_length=100,
        default='heart',
        blank=True,
        help_text="Sticker or icon identifier (e.g., bear, cat, fish, book, heart, star, leaf)"
    )
    title = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Optional letter title (e.g., 未來的我，你好！ / Hello, Future Me!)"
    )
    content = models.TextField(
        help_text="Content of the letter to future self"
    )
    status = models.CharField(
        max_length=20,
        choices=LetterStatus.choices,
        default=LetterStatus.PENDING,
        db_index=True,
        help_text="Letter status: 'pending' (待開啟) or 'opened' (已開啟)"
    )
    opened_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the letter was opened"
    )
    date = models.DateField(
        default=timezone.localdate,
        db_index=True,
        help_text="Date the letter was written"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'My Letter'
        verbose_name_plural = 'My Letters'
        ordering = ['-created_at']

    def __str__(self):
        title_snippet = self.title or self.content[:20]
        return f"{self.user.email} - [{self.status}] {title_snippet}"

    def mark_as_opened(self):
        """
        Transitions the letter from pending to opened and records the timestamp.
        """
        if self.status != LetterStatus.OPENED:
            self.status = LetterStatus.OPENED
            self.opened_at = timezone.now()
            self.save(update_fields=['status', 'opened_at', 'updated_at'])

