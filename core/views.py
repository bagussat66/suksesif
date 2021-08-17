from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    View
)
from django.views.generic.edit import FormView

# from .forms import ProductModelForm
from shop.models import Product,CATEGORY_CHOICES
from .models import Page

import string    
import random  

class HomeView(ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return Page.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            product_list = Product.objects.filter(category=category)
        else:
            product_list = Product.objects.all()

        context['product_list'] = product_list
        context['CATEGORY_CHOICES'] = CATEGORY_CHOICES
        context['category'] =  self.request.GET.get('category') if self.request.GET.get('category') else ''
        return context
