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

from datetime import date

@register.simple_tag(name='percentage_attained')
def percentage_attained(date_from, date_to=None):
    if not date_to:
        date_to = date.today()  # Use today's date if not specified

    if date_to < date_from:
        raise ValueError("`date_to` cannot be earlier than `date_from`.")
    if date.today() > date_to:
        return 100
    total_days = (date_to - date_from).days + 1  # Add 1 to make it inclusive
    attained_days = (date.today() - date_from).days + 1  # Add 1 to make it inclusive
    percentage = attained_days / total_days if total_days else 0.0

    return round(percentage * 100)


register = template.Library()

@register.simple_tag(name='days_between')
def days_between(date1, date2):
    """
    Calculates the number of days between two dates.

    Args:
        date1 (date): The first date.
        date2 (date): The second date.

    Returns:
        int: The number of days between date1 and date2.
    """
    from datetime import date
    if date1 and date2:
        return abs((date2 - date1).days)
    return 0

@register.simple_tag(name='days_passed')
def days_passed(start_date):
    """
    Calculates the number of days passed since the start date.

    Args:
        start_date (date): The start date.

    Returns:
        int: The number of days passed.
    """
    from datetime import date
    if start_date:
        return (date.today() - start_date).days
    return 0

@register.simple_tag(name='days_remaining')
def days_remaining(end_date):
    """
    Calculates the number of days remaining until the end date.

    Args:
        end_date (date): The end date.

    Returns:
        int: The number of days remaining.
    """
    from datetime import date
    if end_date:
        return (end_date - date.today()).days
    return 0

@register.simple_tag(name='percentage_attained')
def percentage_attained(start_date, end_date):
    from datetime import date, timedelta
    today = date.today()
    if start_date and end_date:
        total_days = (end_date - start_date).days + 1  # Include both start and end dates
        days_elapsed = (today - start_date).days + 1
        if total_days > 0:
            percentage = (days_elapsed / total_days) * 100
            return round(percentage)  # Round to two decimal places
    return 0 
