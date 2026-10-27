from django.contrib import admin
from .models import CatTarotDraw


@admin.register(CatTarotDraw)
class CatTarotDrawAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'card_number', 'title_en', 'title_zh', 'created_at')
    list_filter = ('date', 'card_number', 'created_at')
    search_fields = ('user__email', 'title_en', 'title_zh', 'content_en', 'content_zh')
    ordering = ('-date', '-created_at')

