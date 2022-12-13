from django import template
from app_shop.models import Category

register = template.Library()


@register.simple_tag
def get_active_categories():
    """ Возвращает все активные категории товаров """
    return Category.objects.filter(is_active=True)
