from .models import Blog
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

from .models import CATEGORY_CHOICES

import string    
import random  

class BlogListView(ListView):
    template_name = 'blog/list.html'
    paginate_by = 3

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Blog.objects.filter(category=category)
        else:
            return Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)

        context['CATEGORY_CHOICES'] = CATEGORY_CHOICES
        context['category'] =  self.request.GET.get('category') if self.request.GET.get('category') else ''
        return context

class BlogReadView(DetailView):
    model = Blog
    template_name = 'blog/read.html'

    def get_context_data(self, **kwargs):
        context = super(BlogReadView, self).get_context_data(**kwargs)

        context['blog_list'] =  Blog.objects.filter(category=self.object.category)
        return context