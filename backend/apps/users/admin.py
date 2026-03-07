from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserSubscription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name", "last_name", "is_active", "is_verified", "date_joined"]
    list_filter = ["is_active", "is_verified", "is_staff"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-date_joined"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "avatar")}),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser", "is_verified")}),
        ("Push", {"fields": ("fcm_token",)}),
        ("Dates", {"fields": ("date_joined", "last_login")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    readonly_fields = ["date_joined", "last_login"]


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "status", "started_at", "expires_at"]
    list_filter = ["plan", "status"]
    search_fields = ["user__email"]
