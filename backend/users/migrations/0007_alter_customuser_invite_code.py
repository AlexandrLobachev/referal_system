# Generated by Django 4.2.11 on 2024-04-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='invite_code',
            field=models.CharField(max_length=6, unique=True, verbose_name='Инвайт-код для приглашения'),
        ),
    ]
