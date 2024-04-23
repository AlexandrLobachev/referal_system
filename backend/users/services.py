import time
import redis

from referal.settings import (
    REDIS_PASSWORD,
    REDIS_PORT,
    REDIS_HOST,
    LIFE_TIME_CONFIRM_CODE,
    CONFIRM_CODE_DB_NUMBER,
)


client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=CONFIRM_CODE_DB_NUMBER,
    decode_responses=True
)


def save_confirmation_code(phone_number, code):
    """Сохранение кода в Redis."""
    with client:
        client.set(name=phone_number, value=code, ex=LIFE_TIME_CONFIRM_CODE)


def send_confirmation_code_to_phone(phone_number):
    """Отправка кода.

    Генерируем код например: confirmation_code = random.randint(1000, 9999)
    и отправляем на телефон пользователя код подтверждения, однако
    согласоно ТЗ код не отправляем, а имитируем. Код установим '1234'.
    """
    save_confirmation_code(phone_number, 1234)
    time.sleep(3)


def get_control_code(phone_number):
    """Получение кода из БД."""
    with client:
        return client.get(name=phone_number)
