from django import template

register = template.Library()

@register.filter(name='rating_to_stars')
def rating_to_stars(value):
    value = float(value)  # Convert the rating value to a float
    full_star = '<i class="fas fa-star"></i>'
    half_star = '<i class="fas fa-star-half-alt"></i>'
    empty_star = '<i class="far fa-star"></i>'

    full_stars = int(value // 2)
    half_stars = 1 if value % 2 >= 1 else 0  # Adjust the condition to work with a rating out of 10
    empty_stars = 5 - full_stars - half_stars

    stars_html = full_star * full_stars + half_star * half_stars + empty_star * empty_stars
    return stars_html
