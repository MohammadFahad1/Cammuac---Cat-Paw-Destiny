from django.contrib import admin
from .models import Letter


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'sticker', 'status', 'date', 'opened_at', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('user__email', 'title', 'content')
    ordering = ('-created_at',)

