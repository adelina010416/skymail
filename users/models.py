# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from client.models import Client
from constants import nullable


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=250, unique=True, verbose_name='почта')
    phone = models.CharField(max_length=50, unique=True, **nullable, verbose_name='телефон')
    avatar = models.ImageField(upload_to='users/', **nullable, verbose_name='аватар')
    country = models.CharField(max_length=100, **nullable, verbose_name='страна')
    verified_password = models.CharField(verbose_name='ключ для верификации', **nullable)
    clients = models.ManyToManyField(Client)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_active',
             'Can block and unblock users')
        ]
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

