# Generated by Django 5.0.2 on 2024-04-05 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('mailing', '0003_alter_mail_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='recipients',
            field=models.ManyToManyField(to='client.client'),
        ),
    ]
