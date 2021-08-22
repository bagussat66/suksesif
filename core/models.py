from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings

ANIMATION_CHOICES=(
    ('bounceInLeft','Left'),
    ('bounceInRight','Right'),
    ('bounceInUp','Up'),
    ('bounceInDown','Down')
)

class Page(models.Model):
    purpose = models.CharField(max_length=120)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.purpose

class Carousel(models.Model):
    content = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    animation = models.CharField(choices=ANIMATION_CHOICES,max_length=40,default='')
    def __str__(self):
        return self.pk

class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    credential = models.CharField(max_length=120)
    text = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    def __str__(self):
        return self.name