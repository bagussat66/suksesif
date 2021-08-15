from django.urls import path
from .views import TestListView

app_name = 'manager'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
]
