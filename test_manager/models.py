from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings
from shop.models import Item

STATUS_CHOICES = (
    ('A','Aktif'),
    ('I','Selesai'),
    ('D','Diarsip')
)

# Create your models here.
class EnrolledItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(choices=STATUS_CHOICES,max_length=1,default='A')
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title} currently {self.status}"