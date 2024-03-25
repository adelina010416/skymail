from django.db import models

from constants import nullable


# Create your models here.
class Client(models.Model):
    email = models.EmailField(max_length=250, unique=True, verbose_name='почта')
    full_name = models.CharField(max_length=100, verbose_name='полное имя')
    comment = models.TextField(max_length=500, **nullable, verbose_name='комментарий')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
