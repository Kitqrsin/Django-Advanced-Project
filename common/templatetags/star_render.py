from django import template

register = template.Library()

@register.filter
def render_stars(avg):
    full = int(avg) # rounds the number into an int 4.5 => 4
    half = 1 if avg - full >= 0.5 else 0 # checks if there are half stars
    empty = 5 - full - half # empty stars count
    final_result = '★' * full + ('⯪' if half else '') + '☆' * empty if empty < 5 else "No reviews"
    return final_result