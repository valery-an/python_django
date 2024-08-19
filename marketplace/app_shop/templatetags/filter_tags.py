import random
from django import template

register = template.Library()


@register.filter(name='split')
def split(string):
    """ Делит строку по знаку ':' """
    return string.split(':')


@register.filter(name='price_30')
def price_30(price):
    """ Увеличивает цену на 30% """
    price += price * 0.3
    return price


@register.simple_tag
def date_number():
    """ Возвращает день месяца (целое число от 1 до 30) """
    return random.randint(1, 30)


@register.simple_tag
def date_month():
    """ Возвращает краткое название месяца """
    months = ['янв', 'февр', 'март', 'апр', 'май', 'июнь', 'июль', 'авг', 'сент', 'окт', 'нояб', 'дек']
    return random.choice(months)
