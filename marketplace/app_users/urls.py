from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
]
