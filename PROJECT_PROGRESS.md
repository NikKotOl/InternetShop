# Internet Shop (FastAPI)

## Цель проекта

Изучить backend-разработку на Python через создание полноценного интернет-магазина.
Главная цель — понимать архитектуру и причины принятых решений, а не просто получить работающий код.

---

# Стек

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0 (Async)
- Alembic
- Pydantic Settings
- Loguru
- Docker + Docker Compose

---

# Архитектура проекта

app/
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/

---

# Что уже реализовано

## ✅ Этап 1

- Настроен Docker
- Поднят PostgreSQL
- Настроен FastAPI
- Настроены Pydantic Settings
- Настроен SQLAlchemy 2.0
- Настроен AsyncSession
- Настроен Loguru
- Настроен Alembic
- Создана первая модель Category
- Создана первая миграция

---

# Текущий этап

➡ Сейчас начинаем писать CRUD для Category.

Подэтап:

- Pydantic Schemas

---

# Архитектурные правила проекта

- Используем Repository Pattern.
- Используем Service Layer.
- SQL напрямую из роутеров не пишем.
- Изменения структуры БД только через Alembic.
- Пользователь никогда не отправляет служебные поля (id, created_at, is_deleted и т.д.).
- SQLAlchemy модели и Pydantic схемы — разные сущности.

---

# Что уже изучено

Понимаю:

- Docker
- PostgreSQL
- AsyncSession
- Engine
- Connection Pool
- Base.metadata
- __init__.py
- Alembic (базовый уровень)

Пока чувствую неуверенность:

- Alembic
- Repository Pattern (ещё не писали)
- Service Layer (ещё не писали)

---

# Формат обучения

ChatGPT выступает как более опытный backend-разработчик.

Перед написанием нового кода:

1. Сначала обсуждаем проблему.
2. Потом проектируем решение.
3. Затем я предлагаю своё решение.
4. После обсуждения пишем код.

После каждого большого этапа проводится мини-собеседование:
- теория;
- практика;
- архитектурные вопросы.

Главная цель — научиться самостоятельно проектировать backend, а не копировать код.

---

# Последнее обновление

Следующий шаг:

Создать Pydantic-схемы для Category.
