from django.db import models

from user_message.models import Message


class Mail(models.Model):
    FREQUENCY_CHOICES = (('daily', 'раз в день'), ('weekly', 'раз в неделю'), ('monthly', 'раз в месяц'))
    STATUS_CHOICES = (('finished', 'завершена'), ('created', 'создана'), ('started', 'запущена'))

    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=None, verbose_name='сообщение')

    name = models.CharField(max_length=100, verbose_name='название')
    start_time = models.DateTimeField(verbose_name='время старта рассылки')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES,
                                 default='daily', verbose_name='периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='статус')

    def __str__(self):
        return f'{self.name} - c {self.start_time}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
