from django.db import models


# Create your models here.
class Message(models.Model):
    header = models.CharField(max_length=250, verbose_name='тема')
    body = models.CharField(max_length=1000, verbose_name='сообщение')

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
