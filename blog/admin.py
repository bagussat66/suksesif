from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment
from django.contrib import admin

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','content']
    summernote_fields = ('content',)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Comment,CommentAdmin)
admin.site.register(Post,PostAdmin)