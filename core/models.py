from test_core.models import TYPE_CHOICES
from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings
from django_countries.fields import CountryField

# Create your models here.
CATEGORY_CHOICES = (
    ('I','Intelligence'),
    ('H','Mental Health'),
    ('P','Personality')
)

LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)

class Item(models.Model):
    title = models.CharField(max_length=120)
    discount_price = models.IntegerField(blank=True,null=True)
    price = models.IntegerField()
    discounted = models.BooleanField(default=False)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=1)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1)
    description = models.TextField(blank=True,null=True)
    additional_information = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    type = models.CharField(choices=TYPE_CHOICES,blank=True,null=True,max_length=30)
    
    def __str__(self):
        return self.title

    def is_free(self):
        if self.discount_price == 0:
            return True
        else:
            return False
    
    def get_absolute_url(self):
        return reverse('core:product',kwargs={"pk":self.pk})
   
    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart',kwargs={"pk":self.pk})
    
    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart',kwargs={"pk":self.pk})

    def get_subtract_from_cart_url(self):
        return reverse('core:remove-from-cart',kwargs={"pk":self.pk})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        if self.item.discounted:
            return self.quantity * self.item.discount_price
        else:
            return self.quantity * self.item.price

    def get_total_amount_saved(self):
        return self.get_total_item_price()-self.get_total_discount_item_price()

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    citizenship = CountryField(multiple=True)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    charge_id = models.CharField(max_length=100)
    amount = models.FloatField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    discount = models.FloatField(max_length=3)
    min_order = models.FloatField(max_length=100)
    description = models.TextField(blank=True,null=True)
    counter = models.IntegerField(max_length=10,default=0)

    def __str__(self):
        return self.code

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    order_items = models.ManyToManyField(OrderItem)
    start_date= models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(BillingAddress,on_delete=SET_NULL,blank=True,null=True)
    payment = models.ForeignKey(Payment,on_delete=SET_NULL,blank=True,null=True)
    coupon = models.ForeignKey(Coupon,on_delete=SET_NULL,blank=True,null=True)

    def get_total_price(self):
        i = 0
        for order_item in self.order_items.all():
            i += order_item.get_total_discount_item_price()
        
        return i

    def __str__(self):
        return self.user.username

