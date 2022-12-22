from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """ Модель пользователя """
    username = models.CharField(_("username"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    last_name = None
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='телефон')
    avatar = models.ImageField(upload_to='avatars/',
                               default='avatars/no_image.jpg',
                               verbose_name='фотография профиля')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name


class Address(models.Model):
    """ Модель адреса пользователя """
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             verbose_name='пользователь',
                             related_name='addresses')
    name = models.CharField(max_length=50, verbose_name='название')
    region = models.CharField(max_length=150, verbose_name='регион')
    city = models.CharField(max_length=150, verbose_name='город')
    street = models.CharField(max_length=250, verbose_name='улица')
    house_number = models.PositiveIntegerField(verbose_name='номер дома')
    apartment_number = models.PositiveIntegerField(blank=True, verbose_name='номер квартиры')

    class Meta:
        db_table = 'user_addresses'
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'

    def __str__(self):
        return f'{self.region}, г.{self.city}, ул.{self.street}, д.{self.house_number}'
