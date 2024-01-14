from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = [
        'password',
        'last_login',
        # 'groups',
        'meetings',
        'is_superuser',
        'user_permissions',
        'date_joined',
    ]
