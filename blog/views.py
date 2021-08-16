from .models import Post
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

class PostListView(ListView):
    template_name = 'blog/list.html'
    paginate_by = 3

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Post.objects.filter(category=category)
        else:
            return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        context['CATEGORY_CHOICES'] = CATEGORY_CHOICES
        context['category'] =  self.request.GET.get('category') if self.request.GET.get('category') else ''
        return context

class PostReadView(DetailView):
    model = Post
    template_name = 'blog/read.html'

    def get_context_data(self, **kwargs):
        context = super(PostReadView, self).get_context_data(**kwargs)

        context['post_list'] =  Post.objects.filter(category=self.object.category)
        return context