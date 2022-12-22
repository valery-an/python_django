from django import template
from app_shop.models import Category
from services.cart import Cart

register = template.Library()


@register.simple_tag
def get_active_categories():
    """ Возвращает все активные категории товаров """
    return Category.objects.filter(is_active=True)


@register.simple_tag
def get_cart(request):
    return Cart(request)
