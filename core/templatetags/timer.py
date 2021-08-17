from django import template

from django.utils import timezone

register = template.Library()

@register.filter
def remaining_timer(expected):
    td = expected.replace(tzinfo=None)-timezone.now().replace(tzinfo=None)
    h = td.seconds//3600
    m = (td.seconds//60)%60
    s = td.seconds%60
    return f"{h:02}:{m:02}:{s:02}"