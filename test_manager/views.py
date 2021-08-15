from .models import EnrolledProduct, STATUS_CHOICES
from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.

class TestListView(ListView):
    template_name = 'manager/list.html'
    paginate_by = 4

    def get_queryset(self):
        status = self.request.GET.get('status')
        if status:
            return EnrolledProduct.objects.filter(status=status)
        else:
            return EnrolledProduct.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TestListView, self).get_context_data(**kwargs)

        context['STATUS_CHOICES'] = STATUS_CHOICES

        status = self.request.GET.get('status')
        if status:
            context['status'] = status
        else:
            context['status'] = 'A'
        return context