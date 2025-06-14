# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='to_float')
def to_float(value):
    try:
        return float(value)
    except ValueError:
        return None  
