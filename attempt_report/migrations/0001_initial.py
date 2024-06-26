# Generated by Django 5.0.2 on 2024-03-26 16:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mailing', '0002_mail_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='дата и время попытки')),
                ('status', models.CharField(choices=[('successful', 'успешно'), ('unsuccessful', 'не успешно')], max_length=15, verbose_name='статус')),
                ('mail_server_response', models.CharField(blank=True, max_length=250, null=True, verbose_name='ответ почтового сервера')),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mail', verbose_name='рассылка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'попытка',
                'verbose_name_plural': 'попытки',
            },
        ),
    ]
