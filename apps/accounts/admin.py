from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'status', 'is_superuser', 'is_staff', 'is_active', 'created_at')
    list_filter = ('status', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('is_superuser', '-created_at')
    fieldsets = (
        (None, {'fields': ('email', 'status')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')
