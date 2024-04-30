# Create a file called custom_filters.py in your app directory (if it doesn't exist already)
# Define the custom filter in custom_filters.py
from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    return value * arg
