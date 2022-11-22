from django.contrib import admin
from app_users.models import CustomUser, Address


@admin.register(CustomUser)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone_number', 'avatar']


@admin.register(Address)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'region', 'city']
    list_filter = ['user', 'region']
    list_display_links = ['name']
