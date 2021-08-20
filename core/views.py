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
from django.shortcuts import get_object_or_404
# from .forms import ProductModelForm
from shop.models import Product,CATEGORY_CHOICES
from .models import Carousel, Testimonial, Page
from blog.models import Post

import string    
import random  

class HomeView(ListView):
    template_name = 'home.html'

    def get_queryset(self):
        last = Post.objects.filter(hidden=False).order_by('-id')[:6]
        last = reversed(last)
        return last

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['product_list'] = Product.objects.all()
        context['testimonial_list'] = Testimonial.objects.all()
        context['carousel'] = Carousel.objects.all()
        context['welcome'] = get_object_or_404(Page,purpose='welcome')
        context['testimonial'] = get_object_or_404(Page,purpose='testimonial')
        context['shop'] = get_object_or_404(Page,purpose='shop')
        context['blog'] = get_object_or_404(Page,purpose='blog')

        return context
