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
 * PAGINATE_BY (нумерация страниц по количеству данных, `по умолчанию - 100`)

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

## _Заполнение БД тестовыми данными_

Тестовые данные, необходимые для создания моделей, лежат в папке `testdata`.

Для наполнения БД требуется выполнить команду:
```
docker compose exec django python manage.py populate_db
```

Опционально можно передать много параметров, но остановимся на 2-х из них:

* --deadline='05-02-2024' (параметр для дедлайна выших задач)
* --multiplier=3 (множитель, отвечает за количество созданных данных)

По умолчанию, множитель установлен на 1. Для множителя=1 создается 40 проектов, 450 задач и 30 сотрудников.
