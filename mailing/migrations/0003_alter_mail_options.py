# Generated by Django 5.0.2 on 2024-04-02 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_mail_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mail',
            options={'permissions': [('set_status', 'Can finish mails')], 'verbose_name': 'рассылка', 'verbose_name_plural': 'рассылки'},
        ),
    ]