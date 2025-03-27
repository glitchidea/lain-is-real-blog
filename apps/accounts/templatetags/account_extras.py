from django import template
from django.utils.html import strip_tags as django_strip_tags

register = template.Library()

@register.filter
def split(value, arg):
    """Returns the value split by arg."""
    return value.split(arg)

@register.filter
def striptags(value):
    """Alias for the built-in strip_tags function."""
    return django_strip_tags(value)

@register.filter
def strip_tags(value):
    """Removes HTML tags from the input value."""
    return django_strip_tags(value) 