from django.db import models
from django.conf import settings
from django.utils import timezone


class CatTarotDraw(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tarot_draws'
    )
    date = models.DateField(
        default=timezone.localdate,
        db_index=True,
        help_text="Date of the tarot card draw"
    )
    card_number = models.PositiveSmallIntegerField(
        help_text="Selected card number (1, 2, or 3)"
    )
    category_en = models.CharField(
        max_length=100,
        default="Today's Guidance",
        help_text="Category or badge title in English"
    )
    category_zh = models.CharField(
        max_length=100,
        default="今日指引",
        help_text="Category or badge title in Chinese"
    )
    title_en = models.CharField(
        max_length=150,
        help_text="Theme title in English"
    )
    title_zh = models.CharField(
        max_length=150,
        help_text="Theme title in Chinese"
    )
    content_en = models.TextField(
        help_text="Guidance advice in English"
    )
    content_zh = models.TextField(
        help_text="Guidance advice in Chinese"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cat Tarot Draw'
        verbose_name_plural = 'Cat Tarot Draws'
        ordering = ['-date', '-created_at']
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.email} - {self.date} - Card #{self.card_number} ({self.title_en})"

