# Сервис хранения ссылок (закладок) на веб-сайты.
### Технологии:
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/release/python-379/) [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) [![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/) [![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)

## Описание:
- После регистрации в сервисе пользователь может создавать различные коллекции в которые будет добавлять свои закладки.
Одна и та же закладка может быть в одной или нескольких коллекциях сразу, либо быть без коллекции. При добавлении закладки, сервис автоматически получает информацию об Open Graph разметке страницы и добавляет эти данные в базу данных. При отсутствии данной разметки на странице, сохраняется информация из тегов title и meta description (при их наличии).
- Проект запускается в трех контейнерах (nginx, PostgreSQL и Django) через docker-compose.
- Документация API проекта в Swagger приведена по [ссылке](http://localhost/swagger/) (работает при развернутом проекте).

## Как запустить проект локально:

### Клонировать репозиторий и перейти в него:

```sh
git clone https://github.com/Rezenhorn/bookmarks_service.git
```

```sh
cd bookmarks_service/
```

#### Создать файл `.env` в папке `infra/` и заполнить его в соответствии с примером (файл `example.env`).

#### Убедиться, что в системе установлен и запущен Docker.

### Из папки `infra/` запустить Docker:

```sh
cd infra/
```

```sh
docker-compose up -d --build
```

### Выполнить миграции:

```sh
docker-compose exec backend python manage.py migrate
```

### Проект будет запущен по адресу http://localhost/

### Чтобы прекратить работу, необходимо остановить собранные контейнеры (для удаления volumes, можно добавить флаг `-v`):

```sh
docker-compose down
```

## Аутентификация и авторизация пользователей

Аутентификация основана на применении токенов.
- Передайте свой email и пароль в теле запроса на эндпоинт `/auth/users/`. После выполнения запроса, пользователь будет зарегистрирован и внесен в базу данных.
- Далее, чтобы получить токен аутентификации, на эндпоинт `/auth/token/login/` в теле запроса передайте те же данные зарегистрированного пользователя. В ответе вы получите токен.
- Для работы с API, необходимо передавать этот токен вместе с каждым запросом в заголовках запроса в виде `Authorization: Token <ваш токен>`.
- Для удаления токена (выхода из системы), достаточно передать его в заголовке на эндпоинт `/auth/token/logout/`.