from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Regency(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.province.name}: {self.name}"

class District(models.Model):
    name = models.CharField(max_length=100)
    regency = models.ForeignKey(Regency,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.regency.name}: {self.name}"

class Village(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.district.name}: {self.name}"

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=255,null=True)
    zip_code = models.CharField(max_length=100,null=True)
    province = models.ForeignKey(Province,on_delete=models.CASCADE, null=True,default=None)
    regency = models.ForeignKey(Regency,on_delete=models.CASCADE, null=True,default=None)
    district = models.ForeignKey(District,on_delete=models.CASCADE, null=True,default=None)
    default = models.BooleanField(default=False)
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"{self.user.username} in {self.address}"
