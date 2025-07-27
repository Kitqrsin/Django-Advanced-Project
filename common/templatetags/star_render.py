from django import template

register = template.Library()

@register.filter
def render_stars(avg):
    full = int(avg)
    half = 1 if avg - full >= 0.5 else 0
    empty = 5 - full - half
    final_result = '★' * full + ('⯪' if half else '') + '☆' * empty if empty < 5 else "No reviews"
    return final_result