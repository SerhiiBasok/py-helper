from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "user__first_name", "user__last_name"]
    list_filter = ["user", "categories"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
