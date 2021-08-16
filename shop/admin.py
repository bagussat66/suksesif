from django.contrib import admin
from .models import Coupon, Product,CartProduct,Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Cart,CartAdmin)
admin.site.register(Coupon)