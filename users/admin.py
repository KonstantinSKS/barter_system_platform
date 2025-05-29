from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    readonly_fields = (
        'password',
        'is_superuser',
    )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = (
        'id',
        'username',
        'email',
    )
    search_fields = ('username', 'email')
    search_help_text = "Поиск по логину и почте пользователя"
    list_filter = ('username', 'email')
    list_display_links = ('username',)
    ordering = ('id',)
    empty_value_display = '-пусто-'
