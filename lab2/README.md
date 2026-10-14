# ЛР №2. Библиотека в Docker

Проект из ЛР №1, запущенный в Docker. Сущности, эндпоинты, бизнес-правила и тесты те же.

## Файлы Docker

| Файл | Что делает |
|---|---|
| `Dockerfile` | собирает образ приложения: ставит библиотеки, копирует код, при запуске применяет миграции и запускает сервер |
| `.dockerignore` | что не копировать в образ |
| `compose.yaml` | два сервиса (`backend` и `db`), общая сеть `library-net`, том `pgdata` для данных БД |
| `.env.example` | пример переменных окружения |

## Сборка и запуск

```bash
cp .env.example .env
docker compose up --build
```

Swagger: http://localhost:8000/docs

## Остановка

```bash
docker compose down
```

Контейнеры удаляются, а данные остаются в томе `pgdata`.

## Проверка

Состояние контейнеров:
```bash
docker compose ps
```

Тесты внутри контейнера:
```bash
docker compose exec backend pytest -v
```

Сохранность данных:
```bash
curl -X POST localhost:8000/authors -H "Content-Type: application/json" -d '{"name": "Лев Толстой"}'
docker compose down
docker compose up -d
curl localhost:8000/authors
```

Запуск с пустой БД (удаляет том вместе с данными):
```bash
docker compose down -v
docker compose up --build
```
