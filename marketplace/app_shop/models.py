import re
from django.db import models
from django.urls import reverse
from django.utils import timezone
from app_users.models import CustomUser


class Shop(models.Model):
    """ Модель магазина """
    name = models.CharField(max_length=100, verbose_name='название бренда')
    about = models.TextField(max_length=10000, blank=True, verbose_name='о компании')
    logo = models.ImageField(upload_to='logos/', blank=True, verbose_name='логотип')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shops'
        ordering = ['name']
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'


class Category(models.Model):
    """ Модель категории товара """
    name = models.CharField(max_length=100, verbose_name='название')
    icon_path = models.FilePathField(path='media/departments/', verbose_name='символ')
    sorting_index = models.PositiveSmallIntegerField(unique=True, verbose_name='индекс сортировки')
    is_active = models.BooleanField(default=True, verbose_name='активно')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_categories'
        ordering = ['sorting_index']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def get_absolute_url(self):
        return reverse('catalog', args=[self.name])


class Product(models.Model):
    """ Модель товара """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='бренд')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=200, verbose_name='название')
    parameters = models.TextField(max_length=100000, blank=True, verbose_name='характеристики')
    description = models.TextField(max_length=100000, blank=True, verbose_name='описание')
    price = models.PositiveIntegerField(default=0, verbose_name='цена')
    amount = models.PositiveIntegerField(default=0, verbose_name='количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        default_related_name = 'products'
        ordering = ['name']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def get_absolute_url(self):
        return reverse('product', args=[self.id])


def get_upload_path(instance, filename):
    """ Возвращает путь для загрузки изображений товара """
    name = re.sub(r'\W+', ' ', instance.product.name)
    return f'goods/{name}/{filename}'


class ProductImage(models.Model):
    """ Модель изображений товара """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар', related_name='images')
    image = models.ImageField(upload_to=get_upload_path, default='goods/no_image.jpg', verbose_name='изображение')

    class Meta:
        db_table = 'product_images'
        verbose_name = 'изображение товара'
        verbose_name_plural = 'изображения товара'


class Review(models.Model):
    """ Модель отзыва на товар """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    text = models.TextField(max_length=100000, verbose_name='текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        db_table = 'product_reviews'
        default_related_name = 'reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return self.text


class ProductViewed(models.Model):
    """ Модель просмотренных товаров """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    viewed_at = models.DateTimeField(default=timezone.now, verbose_name='дата просмотра')

    class Meta:
        db_table = 'product_viewed'
        default_related_name = 'viewed_products'
        verbose_name = 'просмотренный товар'
        verbose_name_plural = 'просмотренные товары'
        ordering = ['-viewed_at']
