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

# from .forms import ItemModelForm
from shop.models import Item,CATEGORY_CHOICES

import string    
import random  

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
