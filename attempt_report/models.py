from django.db import models

from constants import nullable
from mailing.models import Mail
from users.models import User


# Create your models here.
class Attempt(models.Model):
    STATUS_CHOICES = (('successful', 'успешно'), ('unsuccessful', 'не успешно'))

    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='рассылка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_time = models.DateTimeField(verbose_name='дата и время попытки')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name='статус')
    mail_server_response = models.CharField(max_length=250, **nullable, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'Попытка {self.date_time} - {self.status}'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
