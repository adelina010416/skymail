# Generated by Django 5.0.2 on 2024-04-05 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('mailing', '0004_mail_recipients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='recipients',
            field=models.ManyToManyField(to='client.client', verbose_name='получатели'),
        ),
    ]
