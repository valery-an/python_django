import random
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


@register.simple_tag
def date_number():
    """ Возвращает день месяца (целое число от 1 до 30) """
    return random.randint(1, 30)


@register.simple_tag
def date_month():
    """ Возвращает краткое название месяца """
    months = ['янв', 'февр', 'март', 'апр', 'май', 'июнь', 'июль', 'авг', 'сент', 'окт', 'нояб', 'дек']
    return random.choice(months)