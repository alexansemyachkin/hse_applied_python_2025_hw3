# URL Shortener API

Сервис сокращения ссылок на **FastAPI**.  
Позволяет создавать короткие ссылки, управлять ими и получать статистику использования.

---

# Функциональность

Сервис реализует следующие возможности:

- Создание короткой ссылки
- Редирект по короткой ссылке
- Обновление ссылки
- Удаление ссылки
- Получение статистики переходов
- Поиск по оригинальному URL
- Кастомные alias для ссылок
- Регистрация и логин пользователей
- Кэширование популярных ссылок с использованием Redis

---

# API

## Создание короткой ссылки

POST `/links/shorten`

Body:

```json
{
  "original_url": "https://google.com",
  "custom_alias": "google",
  "expires_at": "2026-12-31T12:00"
}
```

Response:

```json
{
  "short_url": "http://localhost:8000/google"
}
```

---

## Переход по короткой ссылке

GET `/{short_code}`

Пример:

```
http://localhost:8000/abc123
```

Сервис выполняет redirect на оригинальный URL.

---

## Обновление ссылки

PUT `/links/{short_code}`

---

## Удаление ссылки

DELETE `/links/{short_code}`

---

## Получение статистики

GET `/links/{short_code}/stats`

Response:

```json
{
  "original_url": "https://google.com",
  "created_at": "...",
  "click_count": 5,
  "last_used_at": "..."
}
```

---

## Поиск по оригинальному URL

GET `/links/search?original_url=https://google.com`

---

# Авторизация

## Регистрация

POST `/auth/register`

```json
{
  "email": "user@test.com",
  "password": "123456"
}
```

---

## Логин

POST `/auth/login`

```json
{
  "email": "user@test.com",
  "password": "123456"
}
```

---

# Архитектура проекта

```
app/
    main.py
    database.py
    models.py
    schemas.py
    crud.py
    utils.py

    routers/
        links.py
        auth.py

    services/
        cache.py
```

---

# База данных

## Таблица users

| поле | тип |
|-----|-----|
id | int |
email | string |
password_hash | string |
created_at | datetime |

---

## Таблица links

| поле | тип |
|-----|-----|
id | int |
original_url | string |
short_code | string |
created_at | datetime |
expires_at | datetime |
last_used_at | datetime |
click_count | int |
user_id | int |

---

# Кэширование

Для ускорения редиректов используется **Redis**.

Алгоритм работы:

1. При переходе по короткой ссылке проверяется Redis
2. Если ссылка есть в кэшах — выполняется редирект
3. Если ссылки нет — выполняется запрос в PostgreSQL
4. Результат сохраняется в Redis

---

# Запуск проекта

## Через Docker

```bash
docker compose up --build
```

После запуска API будет доступен по адресу:

```
http://localhost:8000
```

Swagger документация:

```
http://localhost:8000/docs
```

Главное: проект развернут на Render!

---
