from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('catalog/<category>/', ProductListView.as_view(), name='catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('product/history/', ProductHistoryListView.as_view(), name='product_history'),
    path('sale/', SaleView.as_view(), name='sale'),
]
