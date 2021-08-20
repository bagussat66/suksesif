from django_summernote.admin import SummernoteModelAdmin
from .models import Page,Carousel, Testimonial
from django.contrib import admin

# Register your models here.

class CoreAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Page,CoreAdmin)
admin.site.register(Carousel,CoreAdmin)
admin.site.register(Testimonial)