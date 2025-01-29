from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Report

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["id", "email", "first_name", "last_name", "is_staff"]
    search_fields = ["email"]
    ordering = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "image", "created_at"]
    search_fields = ["user", "title"]
