from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Address, Coupon, Product,CartProduct,Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Cart,CartAdmin)
admin.site.register(Address)
admin.site.register(Coupon)