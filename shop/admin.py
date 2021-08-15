from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Address, Coupon, Item,CartItem,Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['ordered']

admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Cart,CartAdmin)
admin.site.register(Address)
admin.site.register(Coupon)