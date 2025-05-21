# api_final
api final

# Yatube API

## Описание

Yatube API — это RESTful API для социальной платформы, где пользователи могут публиковать посты, комментировать их, вступать в группы и подписываться на других авторов.
API предоставляет аутентификацию по JWT, поддержку пагинации, фильтрации и прав доступа.

## Установка и запуск проекта

Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/<ваш-логин>/api_final_yatube.git
cd api_final_yatube
```

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Примените миграции и запустите сервер:

```bash
python manage.py migrate
python manage.py runserver
```

## Примеры запросов

Получить список всех постов:

```
GET /api/v1/posts/
```

Создать новый пост (требуется авторизация):

```
POST /api/v1/posts/
```

Получить комментарии к посту:

```
GET /api/v1/posts/{post_id}/comments/
```

Подписка на автора:

```
POST /api/v1/follow/
{
  "following": "username"
}
```

Обновление JWT-токена:

```
POST /api/v1/jwt/refresh/
{
  "refresh": "<ваш refresh токен>"
}
```

## Аутентификация

Используется JWT-аутентификация. Получить токен:

```
POST /api/v1/jwt/create/
{
  "username": "your_username",
  "password": "your_password"
}
```
