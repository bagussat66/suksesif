from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.contrib.auth.models import User


# Create your views here.
class ProfileView(DetailView):
    template_name = 'account/profile/user.html'

    def get_object(self):
        return self.request.user
