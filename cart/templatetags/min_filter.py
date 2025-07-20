from django import template
register = template.Library()

@register.filter
def min_value(a, b):
    return min(a, b)