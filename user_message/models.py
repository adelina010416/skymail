from django.db import models

from constants import nullable
from users.models import User


# Create your models here.
class Message(models.Model):
    header = models.CharField(max_length=250, verbose_name='тема')
    body = models.CharField(max_length=1000, verbose_name='сообщение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **nullable, verbose_name='владелец')

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
