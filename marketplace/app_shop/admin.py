from django.contrib import admin
from app_shop.models import Shop, Category, Product, ProductImage


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'about_short']

    def about_short(self, obj):
        if len(obj.about) > 150:
            return f'{obj.about[:150]}...'
        return obj.about

    about_short.short_description = 'о компании'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sorting_index', 'is_active']
    list_display_links = ['name']
    list_editable = ['is_active']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'amount', 'shop']
    list_filter = ['shop', 'category']
    readonly_fields = ['added_at']
    inlines = [ProductImageInline]
