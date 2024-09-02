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
