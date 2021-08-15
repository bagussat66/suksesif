from test_manager.models import EnrolledProduct
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.http import request
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    View
)
from django.views.generic.edit import FormView
from .forms import CheckoutForm

# from .forms import ProductModelForm
from .models import Address, Coupon, Product, CartProduct, Cart, Transaction,CATEGORY_CHOICES

import string    
import random  

# Create your views here.

class HomeView(ListView):
    template_name = 'home.html'
    paginate_by = 4

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Product.objects.filter(category=category)
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['CATEGORY_CHOICES'] = CATEGORY_CHOICES
        context['category'] =  self.request.GET.get('category') if self.request.GET.get('category') else ''
        return context


class CartSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            context = {
                'object' : order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have active orders")
            return redirect("/")
        
class ProductView(DetailView):
    model = Product
    template_name = 'Product.html'
    
    
class CheckoutView(LoginRequiredMixin,FormView):

    template_name = 'checkout.html'
    form_class = CheckoutForm
    model = Address

    def form_valid(self,form):
        print(form.cleaned_data)
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.info(self.request,"Tidak ada pemesanan aktif.")
            return redirect("core:home")
        
        address = Address(user=self.request.user)
        address.address = form.cleaned_data.get('address')
        address.zip_code = form.cleaned_data.get('zip_code')
        address.save()
        order.address = address
        order.save()
        messages.info(self.request,"Informasi Pembayaran sukses tersimpan.")
        return redirect("shop:transaction",transaction_option=form.cleaned_data.get('transaction_option'))

class TransactionView(View):
    def get(self,*args,**kwargs):
        return render(self.request,"transaction.html")
        
    def post(self,*args,**kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.error(self.request,"Tidak ada pemesanan aktif.")
            return redirect("shop:home")  
        
        amount = order.get_total_price()

        transaction = Transaction(user=self.request.user)
        transaction.amount = amount
        transaction.charge_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) 
        print(transaction.charge_id)

        transaction.save()

        order.ordered = True
        order.transaction = transaction

        for cart_product in order.cart_products.all():
            cart_product.ordered = True
            cart_product.save()

            enrolled_product,create = EnrolledProduct.objects.get_or_create(
                product=cart_product.product,
                user=self.request.user,
                status='A')
            
            if enrolled_product:
                enrolled_product.quantity += cart_product.quantity
                enrolled_product.save()
            else:
                create.quantity = cart_product.quantity
                create.save()

        order.save()
        
        messages.info(self.request,"Pembayaran sukses dilakukan.")

        return redirect("shop:home")
  

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product,create = CartProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False)
    order_query = Cart.objects.filter(user=request.user,ordered=False)
    print(cart_product)
    if order_query.exists():
        order = order_query[0]
        
        if order.cart_products.filter(product__pk=product.pk).exists():
            cart_product.quantity +=1
            cart_product.save()
            messages.info(request,"Produk ditambahkan ke keranjang, jumlah saat ini "+str(cart_product.quantity)+".")
        else:
            order.cart_products.add(cart_product)
            messages.info(request,"Produk ditambahkan ke keranjang")
    else:
        order= Cart.objects.create(user=request.user,ordered_date=timezone.now())
        
        order.cart_products.add(cart_product)
        messages.info(request,"Keranjang baru. Produk ditambahkan ke keranjang. ")
    return redirect("shop:order-summary")

@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    order_query = Cart.objects.filter(user=request.user,ordered=False)
    cart_products = CartProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False)
    
    if order_query.exists():
        order = order_query[0]

        if cart_products.exists():
            cart_product=cart_products[0]
            print(cart_product)
            order.cart_products.remove(cart_product)
            cart_product.delete()
            messages.info(request,"Produk dihapus dari keranjang.")
        else:
            messages.info(request,"Produk tidak ada di keranjang.")
            return redirect("shop:Product", pk=pk)
    else:
        messages.info(request,"Tidak ada pemesanan aktif.")
        return redirect("shop:Product", pk=pk)
    return redirect("shop:order-summary")

@login_required
def subtract_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    order_query = Cart.objects.filter(user=request.user,ordered=False)
    cart_products = CartProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False)
    
    if order_query.exists():

        if cart_products.exists():
            cart_product=cart_products[0]
            cart_product.quantity -=1
            cart_product.save()
            messages.info(request,"Produk dikurangkan dari keranjang, jumlah saat ini  "+str(cart_product.quantity)+".")
        else:
            messages.info(request,"Produk tidak ada di keranjang.")
            return redirect("shop:Product", pk=pk)
    else:
        messages.info(request,"Tidak ada pemesanan aktif.")
        return redirect("shop:Product", pk=pk)
    return redirect("shop:order-summary")

def fetch_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
    except ObjectDoesNotExist:
        messages.error(request,"Kupon tidak berlaku.")
        return redirect("shop:checkout")


def add_coupon_order(request,code):
    try:
        order = Cart.objects.get(user=request.user, ordered=False)
        order.coupon = fetch_coupon(request,code)
        messages.info(request,"Kupon berhasil dipasang.")
        return redirect("shop:checkout")

    except ObjectDoesNotExist:
        messages.error(request,"Tidak ada pemesanan aktif.")
        return redirect("core:home")
    



# class ProductListView(ListView):
#     template_name = 'product/list.html'
#     queryset = Product.objects.all()

# class ProductDetailView(DetailView):
#     template_name = 'product/detail.html'
#     queryset = Product.objects.all()
 
# class ProductCreateView(CreateView):
#     template_name = 'product/create.html'
#     form_class = ProductModelForm
#     queryset = Product.objects.all()

#     def get_success_url(self):
#         return reverse('product:product-list')

#     def form_valid(self,form):
#         print(form.cleaned_data)
#         return super().form_valid(form)

# class productUpdateView(UpdateView):
#     template_name = 'product/update.html'
#     form_class = ProductModelForm
#     queryset = Product.objects.all()
#     def get_success_url(self):
#         return reverse('product:product-list')

#     def form_valid(self,form):
#         print(form.cleaned_data)
#         return super().form_valid(form)

# class productDeleteView(DeleteView):
#     template_name = 'product/delete.html'
#     queryset = Product.objects.all()

#     def get_success_url(self):
#         return reverse('product:product-list')
