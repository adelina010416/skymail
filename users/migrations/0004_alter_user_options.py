# Generated by Django 5.0.2 on 2024-04-02 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_client_alter_user_clients'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('set_active', 'Can block and unblock users')], 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]
