from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('catalog/<int:pk>/', ProductListView.as_view(), name='catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
]
