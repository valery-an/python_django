from django import template

register = template.Library()


@register.filter(name='split')
def split(string):
    """ Делит строку по знаку ':'  """
    return string.split(':')
