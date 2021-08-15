from .models import Blog, Comment
from django.contrib import admin

class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog','content']

admin.site.register(Comment,CommentAdmin)
admin.site.register(Blog)