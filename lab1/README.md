# ЛР №1. REST API «Библиотека»

FastAPI + PostgreSQL + SQLAlchemy (ORM) + Alembic (миграции) + pytest.

## Сущности

- **Автор** (`authors`): имя.
- **Книга** (`books`): название, год, автор, читатель, у которого книга сейчас (пусто — книга в библиотеке).
- **Читатель** (`readers`): имя, email.

Связи: у автора много книг; у читателя может быть много книг.

## Бизнес-правила

1. Нельзя выдать книгу, которая уже выдана.
2. У читателя не может быть больше 3 книг одновременно.

## Запуск

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
docker compose up -d
.venv/bin/alembic upgrade head
.venv/bin/uvicorn app.main:app --reload
```

Swagger: http://localhost:8000/docs

## Эндпоинты

| Метод | Путь | Что делает |
|---|---|---|
| GET | `/authors` | список авторов |
| GET | `/authors/{id}` | один автор |
| POST | `/authors` | создать автора |
| PUT | `/authors/{id}` | изменить автора |
| DELETE | `/authors/{id}` | удалить автора |
| GET | `/books` | список книг |
| GET | `/books/{id}` | одна книга |
| POST | `/books` | создать книгу |
| PUT | `/books/{id}` | изменить книгу |
| DELETE | `/books/{id}` | удалить книгу |
| POST | `/books/{id}/issue/{reader_id}` | выдать книгу читателю |
| POST | `/books/{id}/return` | вернуть книгу |
| GET | `/readers` | список читателей |
| GET | `/readers/{id}` | один читатель |
| POST | `/readers` | создать читателя |
| PUT | `/readers/{id}` | изменить читателя |
| DELETE | `/readers/{id}` | удалить читателя |

Коды ответов: `200` — успешно, `201` — создано, `204` — удалено, `400` — нарушено правило, `404` — не найдено, `422` — неверные данные.

## Тесты

```bash
.venv/bin/pytest -v
```

5 unit-тестов (`tests/test_unit.py`) проверяют валидацию данных, 3 integration-теста (`tests/test_integration.py`) проверяют API вместе с базой. Тесты работают с отдельной базой `library_test`.
