from django.contrib import admin
from .models import DiaryNote


@admin.register(DiaryNote)
class DiaryNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'icon', 'created_at')
    list_filter = ('date', 'icon', 'created_at')
    search_fields = ('user__email', 'note', 'icon')
    ordering = ('-date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')

