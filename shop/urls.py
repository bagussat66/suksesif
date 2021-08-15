from django.urls import path
from .views import HomeView, TransactionView,ItemView,CheckoutView,CartSummaryView, add_coupon_order,add_to_cart,remove_from_cart,subtract_from_cart

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('Item/<int:pk>/', ItemView.as_view(), name='Item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', CartSummaryView.as_view(), name='order-summary'),
    path('transaction/<transaction_option>', TransactionView.as_view(), name='transaction'),
    path('add-to-cart/<int:pk>/',add_to_cart, name='add-to-cart'),
    path('add-coupon-order/<int:pk>/',add_coupon_order, name='add-coupon-order'),
    path('subtract-from-cart/<int:pk>/',subtract_from_cart, name='subtract-from-cart'),
    path('remove-from-cart/<int:pk>/',remove_from_cart, name='remove-from-cart')
]
