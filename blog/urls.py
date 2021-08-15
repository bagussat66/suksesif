from django.urls import path
from .views import BlogListView,BlogReadView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', BlogReadView.as_view(), name='blog-read'),
]
