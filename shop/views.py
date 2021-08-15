from test_manager.models import EnrolledItem
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

# from .forms import ItemModelForm
from .models import Address, Coupon, Item, CartItem, Cart, Transaction,CATEGORY_CHOICES

import string    
import random  

# Create your views here.

class HomeView(ListView):
    template_name = 'home.html'
    paginate_by = 4

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Item.objects.filter(category=category)
        else:
            return Item.objects.all()

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
        
class ItemView(DetailView):
    model = Item
    template_name = 'Item.html'
    
    
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

        for cart_item in order.cart_items.all():
            cart_item.ordered = True
            cart_item.save()

            enrolled_item,create = EnrolledItem.objects.get_or_create(
                item=cart_item.item,
                user=self.request.user,
                status='A')
            
            if enrolled_item:
                enrolled_item.quantity += cart_item.quantity
                enrolled_item.save()
            else:
                create.quantity = cart_item.quantity
                create.save()

        order.save()
        
        messages.info(self.request,"Pembayaran sukses dilakukan.")

        return redirect("shop:home")
  

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart_item,create = CartItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_query = Cart.objects.filter(user=request.user,ordered=False)
    print(cart_item)
    if order_query.exists():
        order = order_query[0]
        
        if order.cart_items.filter(item__pk=item.pk).exists():
            cart_item.quantity +=1
            cart_item.save()
            messages.info(request,"Produk ditambahkan ke keranjang, jumlah saat ini "+str(cart_item.quantity)+".")
        else:
            order.cart_items.add(cart_item)
            messages.info(request,"Produk ditambahkan ke keranjang")
    else:
        order= Cart.objects.create(user=request.user,ordered_date=timezone.now())
        
        order.cart_items.add(cart_item)
        messages.info(request,"Keranjang baru. Produk ditambahkan ke keranjang. ")
    return redirect("shop:order-summary")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)

    order_query = Cart.objects.filter(user=request.user,ordered=False)
    cart_items = CartItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)
    
    if order_query.exists():
        order = order_query[0]

        if cart_items.exists():
            cart_item=cart_items[0]
            print(cart_item)
            order.cart_items.remove(cart_item)
            cart_item.delete()
            messages.info(request,"Produk dihapus dari keranjang.")
        else:
            messages.info(request,"Produk tidak ada di keranjang.")
            return redirect("shop:Item", pk=pk)
    else:
        messages.info(request,"Tidak ada pemesanan aktif.")
        return redirect("shop:Item", pk=pk)
    return redirect("shop:order-summary")

@login_required
def subtract_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)

    order_query = Cart.objects.filter(user=request.user,ordered=False)
    cart_items = CartItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)
    
    if order_query.exists():

        if cart_items.exists():
            cart_item=cart_items[0]
            cart_item.quantity -=1
            cart_item.save()
            messages.info(request,"Produk dikurangkan dari keranjang, jumlah saat ini  "+str(cart_item.quantity)+".")
        else:
            messages.info(request,"Produk tidak ada di keranjang.")
            return redirect("shop:Item", pk=pk)
    else:
        messages.info(request,"Tidak ada pemesanan aktif.")
        return redirect("shop:Item", pk=pk)
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
    



# class ItemListView(ListView):
#     template_name = 'item/list.html'
#     queryset = Item.objects.all()

# class ItemDetailView(DetailView):
#     template_name = 'item/detail.html'
#     queryset = Item.objects.all()
 
# class ItemCreateView(CreateView):
#     template_name = 'item/create.html'
#     form_class = ItemModelForm
#     queryset = Item.objects.all()

#     def get_success_url(self):
#         return reverse('item:item-list')

#     def form_valid(self,form):
#         print(form.cleaned_data)
#         return super().form_valid(form)

# class itemUpdateView(UpdateView):
#     template_name = 'item/update.html'
#     form_class = ItemModelForm
#     queryset = Item.objects.all()
#     def get_success_url(self):
#         return reverse('item:item-list')

#     def form_valid(self,form):
#         print(form.cleaned_data)
#         return super().form_valid(form)

# class itemDeleteView(DeleteView):
#     template_name = 'item/delete.html'
#     queryset = Item.objects.all()

#     def get_success_url(self):
#         return reverse('item:item-list')
