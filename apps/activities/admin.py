from django.contrib import admin
from .models import DailyCheckIn, Alarm


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'lucky_number', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'time', 'period', 'title_zh', 'title_en', 'enabled', 'created_at')
    list_filter = ('period', 'enabled', 'created_at')
    search_fields = ('user__email', 'title_zh', 'title_en')
    ordering = ('id',)
    readonly_fields = ('created_at', 'updated_at')
