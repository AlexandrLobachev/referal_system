from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import RetrieveUpdateAPIView

from users.services import send_confirmation_code_to_phone, get_control_code
from .serializers import (
    PhoneNumberSerializer,
    GetTokenSerializer,
    ProfileSerializer
)
from referal.settings import LIFE_TIME_CONFIRM_CODE

User = get_user_model()


class ProfileView(RetrieveUpdateAPIView):
    """Получение или редактирование профиля."""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class SignupView(APIView):
    """Отправляет confirmation code."""

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data['phone_number']
        send_confirmation_code_to_phone(phone_number)
        return Response(
            {'message':
                 (f'Код подтверждения отправлен на телефон {phone_number}, '
                  f'и будет действителен {int(LIFE_TIME_CONFIRM_CODE/60)} минут')},
            status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """Возвращает JWT-токен в обмен на phone_number и confirmation code."""

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = str(serializer.validated_data.get('phone_number'))
        confirmation_code = serializer.validated_data.get('confirmation_code')
        control_code = get_control_code(phone_number)
        if not control_code:
            message = {'message': 'Код для этого телефона отсутвует!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if control_code != confirmation_code:
            message = {'message': 'Код подтверждения невалиден!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(phone_number=phone_number)
        token = AccessToken.for_user(user)
        message = {'token': str(token)}
        return Response(message, status=status.HTTP_200_OK)
