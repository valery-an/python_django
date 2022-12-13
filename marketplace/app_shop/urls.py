from django.urls import path
from .views import *

urlpatterns = [
    path('', main_view, name='main'),
    path('catalog/<int:pk>/', ProductListView.as_view(), name='catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
]
