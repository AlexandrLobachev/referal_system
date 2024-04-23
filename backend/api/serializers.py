from rest_framework.serializers import Serializer, CharField, SerializerMethodField, ModelSerializer, ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from referal.settings import CONF_CODE_MAX_LENGHT
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneNumberSerializer(Serializer):
    """Сериализатор номера телефона."""

    phone_number = PhoneNumberField()


class ProfileSerializer(ModelSerializer):
    """Сериализатор профиля."""

    users_with_my_invite = SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'phone_number',
            'invite_code',
            'other_invite_code',
            'users_with_my_invite',
        )
        read_only_fields  = ('id', 'phone_number')

    def validate_other_invite_code(self, other_invite_code):
        if self.instance.other_invite_code:
            raise ValidationError('Инвайт-код уже применен.')
        if self.instance.invite_code == other_invite_code:
            raise ValidationError('К себе нельзя применить свой инвайт-код.')
        if User.objects.filter(invite_code=other_invite_code):
            return other_invite_code
        raise ValidationError(
            'Инвайт-код не действителен.')

    def get_users_with_my_invite(self, user):
        qs = User.objects.filter(other_invite_code=user.invite_code)
        return PhoneNumberSerializer(qs, many=True).data


class GetTokenSerializer(Serializer):
    """Сериализатор получения токена."""

    phone_number = PhoneNumberField()
    confirmation_code = CharField(max_length=CONF_CODE_MAX_LENGHT)