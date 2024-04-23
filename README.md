#  Blog-platform

## Описание

API реферальной системы.

## Автор:

[Александр Лобачев](https://github.com/AlexandrLobachev/)

## Технологии используемые в проекте:

Python, Django, DRF, Nginx, Docker, Gunicorn, PostgreSQL, Redis

## Как запустить проект локально:

Для запуска на Windows вам потребуеться установить Docker и WSL.
Скачать можно с официального сайта и там же есть инструкции.

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:AlexandrLobachev/referal_system.git
```
```
cd referal_system
```
Создать файл .env и заполнить его(пример заполнения можно взять ниже):
```
POSTGRES_DB=referal_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY = 'django-insecure-(4f*^&o%pql#jpm$$*ba907w658@6_mhw7u_dt=1@yj=!f-e*-'
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1 localhost

REDIS_PASSWORD=redispass
REDIS_PORT=6379
REDIS_HOST=redis
```
Создать образы и запустить контейнеры командой:
```
docker compose up -d
```
Выполните миграции
```
docker compose exec backend python manage.py migrate
```
Соберите статические файлы
```
docker compose exec backend python manage.py collectstatic
```
Скопируйте статические файлы
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
Создать суперпользователя
```
docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

Проект доступен по адресу:
```
http://127.0.0.1:8000/
```
API проекта по адресу:
```
http://127.0.0.1:8000/api/
```
Панель администратора по адресу:
```
http://127.0.0.1:8000/admin/
```

# Тестирование через Postman:
В директории postman-collection сохранена коллекция тестовых запросов для API.

## Примеры запросов:

### Запрос на получение кода по смс: 
POST http://127.0.0.1:8000/api/auth/signup/

```
{
    "phone_number": "+79831233223"
}
```

### Запрос на получение кода: 
POST http://127.0.0.1:8000/api/auth/token/

Запрос должен содержать номер на который отправлен код и код.
#### В режиме разработки смс не отправляеться, вводить код "1234"

```
{
    "phone_number": "+79831233223",
    "confirmation_code": "1234"
}
```

### Запрос на получение профиля: 
GET http://127.0.0.1:8000/api/profile/

В заголовке необходимо передать токен, например:

'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90...'

Пример ответа:
```
{
    "id": 1,
    "username": "User_1sfuXs",
    "phone_number": "+79831233223",
    "invite_code": "1sfuXs",
    "other_invite_code": null,
    "users_with_my_invite": [
        {
            "phone_number": "+79833550002"
        },
        {
            "phone_number": "+79833550003"
        }
    ]
}
```

### Редактирование профиля:
Для ректирования профиля доступны поля: "username": "User_1sfuXs" неограниченное количество раз и "other_invite_code" единовременно.

PATCH http://127.0.0.1:8000/api/profile/
```
{
    "username": "NewUsername",
    "other_invite_code": "TbM6wJ"
}
```
Пример ответа:
```
{
    "id": 1,
    "username": "NewUsername",
    "phone_number": "+79831233223",
    "invite_code": "1sfuXs",
    "other_invite_code": "TbM6wJ",
    "users_with_my_invite": [
        {
            "phone_number": "+79833550002"
        },
        {
            "phone_number": "+79833550003"
        }
    ]
}
```
