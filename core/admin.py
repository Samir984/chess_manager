from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.db import transaction
from django.http.request import HttpRequest

from .models import Report
from .models import Profile
from .models import Match
from .models import Transaction




from .models import Token

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["id", "email", "first_name", "last_name", "is_staff","image"]
    search_fields = ["email"]
    ordering = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin[Profile]):
    list_display = ["id", "user", "no_of_games_played", "coins", "game_point", "created_at"]
    search_fields = ["user__email"]
    list_filter = ["created_at", "updated_at"]



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
    

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin[Match]):
    list_display = ["id","bet_amount","is_bet",  "is_quit","is_draw", "player_white", "player_black","winner_player","quitter_player", "unexpected_leaver_player","is_completed", "is_quit",  "created_at","end_at"]
    search_fields = ["id","player_white", "player_black"]
    list_filter = ["is_completed", "is_quit", "is_bet", "is_draw"]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin[Transaction]):
    list_display = ["id", "user", "amount","description"]
    search_fields = ["user","amount"]

    def save_model(self, request:HttpRequest, obj:Transaction, form:ModelForm, change:bool):
        user=obj.user
        if not request.user.is_superuser:
            raise PermissionDenied(_("Only superusers can add or modify transactions."))
        
        if obj.amount > 1000:
            raise PermissionDenied(_("Transaction amount cannot exceed $1000."))

        
        with transaction.atomic():
            user.profile.coins = user.profile.coins + obj.amount
            user.profile.save()
            super().save_model(request, obj, form, change)

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
            raise PermissionDenied("Only admin users can create tokens")
