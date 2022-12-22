from django.contrib import admin
from app_users.models import CustomUser, Address
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['first_name', 'email', 'phone_number', 'avatar']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'region', 'city']
    list_filter = ['user', 'region']
    list_display_links = ['name']
