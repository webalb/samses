from django import template
import math
import datetime

register = template.Library()

@register.filter
def readable_day_count(day_count):
    """
    Converts a number of days into a human-readable format (mm months, dd days).

    Args:
        day_count: The number of days.

    Returns:
        A string representing the day count in a human-readable format.
    """

    months = math.floor(day_count / 30)
    days = day_count % 30

    if months == 0:
        return f"{days} days"
    elif days == 0:
        return f"{months} months"
    else:
        return f"{months} months, {days} days"

@register.simple_tag
def max_days(date_to, date_from):
    return (date_to - date_from).days
    
@register.simple_tag 
def days_attained(date_from):
    d = (datetime.date.today() - date_from).days
    return d if d > 0 else 0

@register.filter
def none(value):
    """Returns 'Not Available' if the value is None or empty."""
    return value if value else "Not Available"

@register.filter
def none_or_percentage(value):
    """
    Returns 'Not Available' if the value is None or empty.
    Appends '%' to integers or floats, rounding floats to whole numbers.
    """
    return "Not Available" if value in [None, ''] else f"{int(value)}%"