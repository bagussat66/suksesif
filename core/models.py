from blog.models import Post
from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings

class Page(models.Model):
    purpose = models.CharField(max_length=120)
    blog = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.purpose

class Carousel(models.Model):
    text = models.CharField(max_length=120)
    image = models.ImageField(blank=True,null=True)
    def __str__(self):
        return self.text