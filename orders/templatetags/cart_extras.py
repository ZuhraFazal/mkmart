
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply two values"""
    try:
        return int(value) * int(arg)
    except:
        return 0
