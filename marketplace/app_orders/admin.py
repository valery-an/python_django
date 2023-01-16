from django.contrib import admin
from app_orders.models import Delivery, Order, OrderItem


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['type', 'price', 'min_order_cost']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cost', 'status', 'delivery']
    list_filter = ['user', 'status', 'delivery']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline]
