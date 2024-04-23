import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
from referal.settings import INVITE_CODE_LENGHT


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(
        'Номер телефона',
        unique=True,
    )
    invite_code = models.CharField(
        'Инвайт-код для приглашения',
        max_length=INVITE_CODE_LENGHT,
        unique=True,
    )
    other_invite_code = models.CharField(
        'Инвайт-код пригласившего',
        max_length=INVITE_CODE_LENGHT,
        blank=True,
        null=True,
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phone_number)


@receiver(pre_save, sender=CustomUser)
def add_unique_code(sender, instance, **kwargs):
    if instance.invite_code and instance.username:
        return
    code = ''.join(random.choices(
        string.ascii_letters + string.digits, k=INVITE_CODE_LENGHT
    ))
    if not instance.invite_code:
        instance.invite_code = code
    if not instance.username:
        instance.username = f'User_{code}'
