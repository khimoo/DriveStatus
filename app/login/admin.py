from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_main",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("is_main",)}),)


User = get_user_model()
admin.site.register(User, CustomUserAdmin)
