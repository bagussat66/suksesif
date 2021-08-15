from test_core.models import TYPE_CHOICES
from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings

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

class Product(models.Model):
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
        return reverse('shop:Product',kwargs={"pk":self.pk})
   
    def get_add_to_cart_url(self):
        return reverse('shop:add-to-cart',kwargs={"pk":self.pk})
    
    def get_remove_from_cart_url(self):
        return reverse('shop:remove-from-cart',kwargs={"pk":self.pk})

    def get_subtract_from_cart_url(self):
        return reverse('shop:remove-from-cart',kwargs={"pk":self.pk})

class CartProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        if self.product.discounted:
            return self.quantity * self.product.discount_price
        else:
            return self.quantity * self.product.price

    def get_total_amount_saved(self):
        return self.get_total_product_price()-self.get_total_discount_product_price()

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
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

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    cart_products = models.ManyToManyField(CartProduct)
    start_date= models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(Address,on_delete=SET_NULL,blank=True,null=True)
    transaction = models.ForeignKey(Transaction,on_delete=SET_NULL,blank=True,null=True)
    coupon = models.ForeignKey(Coupon,on_delete=SET_NULL,blank=True,null=True)

    def get_total_price(self):
        i = 0
        for cart_product in self.cart_products.all():
            i += cart_product.get_total_discount_product_price()
        
        return i

    def __str__(self):
        return self.user.username

