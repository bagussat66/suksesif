from django_summernote.admin import SummernoteModelAdmin

from django.contrib import admin
from .models import Coupon, Product,CartProduct,Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('description','additional_information')

admin.site.register(Product,ProductAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart,CartAdmin)
admin.site.register(Coupon)