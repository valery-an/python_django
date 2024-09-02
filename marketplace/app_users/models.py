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
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.first_name
