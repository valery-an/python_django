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
    list_display = ['id', 'user', 'cost', 'is_paid', 'delivery']
    list_editable = ['is_paid']
    list_filter = ['user', 'delivery']
    inlines = [OrderItemInline]
