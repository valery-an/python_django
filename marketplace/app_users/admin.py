from django.contrib import admin
from app_users.models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['first_name', 'email', 'phone_number', 'avatar']
