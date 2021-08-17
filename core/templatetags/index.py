from django import template

from django.utils import timezone

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def list(objects):
    return list(objects)
