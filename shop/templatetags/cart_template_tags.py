from django import template
from shop.models import Cart

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user,ordered=False)
        if qs.exists():
            i = 0
            for order_item in qs[0].order_items.all():
                i += order_item.quantity
            return i