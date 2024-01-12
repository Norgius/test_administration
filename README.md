# Тестовое

Все настройки и секреты требуется хранить в файле `.env`, который нужно создать в корневой директории проекта.

Для подключения к `PostgreSQL` укажите следующие настройки:
 * POSTGRES_USER
 * POSTGRES_PASSWORD
 * POSTGRES_DB

Секреты `Django`:
 * SECRET_KEY
 * ALLOWED_HOSTS
 * POSTGRES_DSN (пример: `postgres://postgres:postgres@db:5432/postgres`)
 * DEBUG
 * PAGINATION_BY (нумерация страниц по количеству данных, `по умолчанию - 100`)

## _Development_

Скачайте и соберите докер-образы с помощью Docker Сompose:
```sh
$ docker compose pull --ignore-buildable
$ docker compose build
```

Запустите докер-контейнеры и не выключайте:
```sh
$ docker compose up
```

Примените миграции:
```sh
$ docker compose run --rm django python manage.py migrate
```

И создайте нового суперпользователя:
```sh
$ docker compose run --rm django python manage.py createsuperuser
```

## _Production_

Находясь в корневой директории проекта создайте каталог `static`:
```sh
mkdir static
```

Перейдите в директорию `docker_production/`. Дополните `nginx.conf` вашим `ip` или `доменом`:
```sh
server_name ***********;
```

Оставаясь в этой же директории повторите те же шаги, что указаны в _`Development`_.
