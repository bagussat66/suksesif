from django.urls import path
from .views import PostListView,PostReadView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>/', PostReadView.as_view(), name='read'),
]
