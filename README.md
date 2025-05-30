# barter_system_platform (тестовое задание)

## Описание

barter_system_platform — это бэкенд приложение на Django для обмена вещами между пользователями. Пользователи могут размещать объявления, просматривать другие объявления и отправлять предложения обмена. Приложение реализовано с использованием REST API на DRF.

### Реализовано:
* Создание, редактирование и удаление объявлений с ограничением по авторству.
* Поиск и фильтрация объявлений по категориям, состоянию и ключевым словам.
* Создание и обновление статусов предложений обмена между пользователями.
* Доступ к API для всех операций с объявлениями и предложениями.
* Регистрация пользователя в системе по логину, почте и паролю.
* Авторизация пользователя по токену 'rest_framework.authtoken'.
* Реализовано тестирование на Pytest: модели, сериализаторы, API-вью. Покрытие кода >90%.
* Swagger/Редок-документация через drf-spectacular.
* Админ-панель для управлениями пользователями, объявлениями (категории, объявления, предложения обмена).

## Технологии:
* Python 3.12
* Django 5.1
* Djangorestframework 3.15
* DRF Spectacular
* SQLite3 (local) / PostgreSQL (Docker)
* Pytest + pytest-django + coverage
* Docker + docker-compose + Nginx

## Установка и запуск проекта:
Клонировать репозиторий:
```
git clone https://github.com/KonstantinSKS/barter_system_platform.git
```
или по shh-ключу:
```
git clone git@github.com:KonstantinSKS/barter_system_platform.git
```
Перейти в папку с проектом
```
cd barter_system_platform
```
В корне проекта создать файл .env
```
touch .env
```
и заполнить его по образцу файла .env.template.

### Вариант 1: Локальный запуск (SQLite)
В .env-файле установить `DOCKER=False`.

Cоздать и активировать виртуальное окружение:
```
py -3.12 -m venv venv
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Создать супрепользователя для доступа в админ-панель:
```
python manage.py createsuperuser
```
Запустить проект:
```
python manage.py runserver
```
Перейти в админ-панель http://127.0.0.1:8000/admin/ (авторизация по вашему логину и паролю созданным для супрепользователя)
и создать категории для объявлений (http://127.0.0.1:8000/admin/ads/category/add/).

### Вариант 2: Запуск в Docker
В .env-файле установить `DOCKER=True`.

```
docker compose up -d --build
```

### Cупрепользователь (логин: admin, пароль: admin) и две тестовые категории объявлений будут созданы автоматически при запуске.


## После запуска проекта документация к API и примеры запросов будут доступны по ссылкам:
* [http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)
* [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
* админ-панель [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)


## Примеры API-запросов

### Регистрация

`POST /api/registration/`

```json
{
  "username": "newuser",
  "email": "new@mail.com",
  "password": "StrongPass123"
}
```

### Вход

`POST /api/login/`

```json
{
  "username": "newuser",
  "password": "StrongPass123"
}
```

### Создание объявления

`POST /api/ads/`

```json
{
  "title": "Книга",
  "description": "Старое издание",
  "category": 1,
  "condition": "used"
}
```

### Получение объявлений

`GET /api/ads/?search=книга&condition=used&category=Книги`

### Создание предложения

`POST /api/proposals/`

```json
{
  "ad_sender": 1,
  "ad_receiver": 2,
  "comment": "Обменяемся?"
}
```

### Авторизация пользователя по токену
Чтобы создавать объявления и предложения авторизуйтесь в системе по токену.
Для этого на странице http://127.0.0.1:8000/api/swagger/ нажмите "Authorize" 
и в окне введите префикс "Token" (без кавычек) и через пробел ваш токен, полученный при логине.


## Автор:
Стеблев Константин
