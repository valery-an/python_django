from django import forms
from django.db import models
from app_users.models import AbstractUser
from app_shop.models import Product


class Review(models.Model):
    user = models.ForeignKey(AbstractUser, on_delete=models.CASCADE,
                             verbose_name='пользователь', related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='товар', related_name='reviews')
    name = models.CharField(max_length=150, blank=True, verbose_name='подпись')
    email = models.EmailField(blank=True, verbose_name='email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    text = models.TextField(max_length=10000, verbose_name='отзыв')

    class Meta:
        db_table = 'product_reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'name', 'email')
