from django.contrib import admin
from app_shop.models import Shop, Category, SubCategory, Product


@admin.register(Shop)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['name', 'about_short']

    def about_short(self, obj):
        if len(obj.about) > 150:
            return f'{obj.about[:150]}...'
        return obj.about

    about_short.short_description = 'о компании'


@admin.register(Category)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['name', 'sorting_index', 'is_active']
    list_display_links = ['name']
    list_editable = ['is_active']


@admin.register(SubCategory)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(Product)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'subcategory', 'price', 'amount', 'shop']
    list_filter = ['shop', 'category']
