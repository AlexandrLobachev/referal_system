# Generated by Django 4.2.11 on 2024-04-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='other_invite_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Инвайт-код пригласившего'),
        ),
    ]
