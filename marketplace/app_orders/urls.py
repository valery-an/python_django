from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:pk>/', add_product_to_cart, name='add_product'),
    path('cart/reduce/<int:pk>/', reduce_product_from_cart, name='reduce_product'),
    path('cart/remove/<int:pk>/', remove_product_from_cart, name='remove_product'),
    path('create/', create_order_view, name='create_order'),
    path('payment/<int:pk>/', payment_view, name='payment'),
    path('history/', OrderListView.as_view(), name='order_history'),
    path('<int:pk>/', OrderDetailView.as_view(), name='one_order'),
]
