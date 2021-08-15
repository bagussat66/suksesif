from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings

# Create your models here.
CATEGORY_CHOICES = (
    ('F','Finansial'),
    ('C','Karir'),
    ('P','Psikologi')
)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    content = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return f"{self.content} of {self.user.name}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.user.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=120)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=1)
    content = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    image_caption = models.CharField(max_length=120)
    comment_disabled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    comments = models.ManyToManyField(Comment,blank=True)
    likes = models.ManyToManyField(Like,blank=True)
    
    def __str__(self):
        return self.title

