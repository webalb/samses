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

from datetime import date

@register.simple_tag
def percentage_attained(date_from, date_to=None):
  """
  Calculates the percentage of days attained from `date_from` (inclusive)
  to `date_to` (exclusive, defaults to today if not provided).

  Args:
      date_from (date): The start date (inclusive).
      date_to (date, optional): The end date (exclusive). Defaults to None,
          which means the calculation will be done up to today.

  Returns:
      float: The percentage of days attained, expressed as a decimal between 0.0
          (no days attained) and 1.0 (all days attained).

  Raises:
      ValueError: If `date_to` is earlier than `date_from`.
  """

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
