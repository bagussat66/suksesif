from django.contrib import admin
from .models import ShippingAddress, District, Province, Regency, Village

admin.site.register(Province)
admin.site.register(Regency)
admin.site.register(District)
admin.site.register(Village)
admin.site.register(ShippingAddress)
