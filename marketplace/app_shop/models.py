from django.db import models


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
    icon_path = models.FilePathField(path='static/assets/img/icons/departments/', verbose_name='символ')
    sorting_index = models.PositiveSmallIntegerField(unique=True, verbose_name='индекс сортировки')
    is_active = models.BooleanField(default=True, verbose_name='активно')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_categories'
        ordering = ['sorting_index']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """ Модель товара """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             verbose_name='бренд', related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='категория', related_name='products')
    name = models.CharField(max_length=200, verbose_name='название')
    short_description = models.CharField(max_length=10000, blank=True, verbose_name='краткое описание')
    description = models.TextField(max_length=100000, blank=True, verbose_name='описание')
    price = models.PositiveIntegerField(default=0, verbose_name='цена')
    image = models.ImageField(upload_to='goods/', default='goods/no_image.png', verbose_name='изображение')
    amount = models.PositiveIntegerField(default=0, verbose_name='количество')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        ordering = ['name']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
