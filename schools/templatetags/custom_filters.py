from django import template
import math

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
