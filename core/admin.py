from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.http.request import HttpRequest

from .models import Report
from .models import Token

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


from django.utils.html import format_html

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin[Report]):
    list_display = ["id", "user", "title", "imageLink", "is_solved", "created_at"]
    search_fields = ["user", "title"]
    
    @admin.display(description="imageURL")
    def imageLink(self, obj:Report):
        if obj.imageURL:
         return format_html('<a href="{}" target="_blank">View Image</a>', obj.imageURL)
        else:
         return "-"
    


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin[Token]):
    list_display = ["id", "user", "key"]
    search_fields = ["user"]

    def save_model(
        self, request: HttpRequest, obj: Token, form: ModelForm, change: bool
    ):
        if request.user.is_superuser:  # type: ignore
            super().save_model(request, obj, form, change)
        else:
            raise PermissionError("Only admin users can create tokens")
