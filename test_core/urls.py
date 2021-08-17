
from django.urls import path
from .views import TestPageView, TesterUpdateView, TestResultView

app_name = 'test'

urlpatterns = [
    path('<type>/tester/', TesterUpdateView.as_view(), name='tester'),
    path('<type>/result/', TestResultView.as_view(), name='result'),
    path('<type>/<no>/', TestPageView.as_view(), name='assessment'),
    path('<type>/', TestPageView.as_view(),{'no':'1'}, name='assessment'),
]
