# ПОВОРОТ — MVP Telegram-бот игры

Rule-based Telegram-бот на Python для 4-ходовой сюжетной игры без LLM в рантайме.

## Что умеет MVP
- Сбор 4 вводов: имя, предмет, локация, страх.
- Анализ имени по правилам (formality/oddness/compactness/duality).
- Нормализация сущностей через exact/case-insensitive/fuzzy (RapidFuzz).
- Выбор каркаса: Defense/Growth/Startup/Recovery.
- Назначение роли, угрозы, модификатора.
- Стартовая карточка с объяснением «Почему так вышло».
- Матч на 4 хода с 4 статами: Прогресс, Риск, Репутация, Ресурс.
- Поддержка кнопок и свободного текстового хода.
- Rule-based концовка из 12 вариантов.

## Стек
- Python 3.11+
- aiogram 3.x
- SQLAlchemy async 2.x
- PostgreSQL
- Pydantic
- RapidFuzz
- Docker / docker-compose

## Запуск через Docker Compose
1. Скопируйте env:
```bash
cp .env.example .env
```
2. Заполните `BOT_TOKEN` в `.env`.
3. Запуск:
```bash
docker compose up --build
```

## Локальный запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# поправьте DATABASE_URL на localhost, например:
# postgresql+asyncpg://povorot:povorot@localhost:5432/povorot
python -m app.main
```

## ENV
- `BOT_TOKEN` — токен Telegram-бота.
- `DATABASE_URL` — async SQLAlchemy URL.
- `LOG_LEVEL` — уровень логов.

## Контент
Контент хранится в `app/content/*.json`:
- сущности (`items`, `locations`, `fears`, `roles`, `threats`, `modifiers`)
- каркасы, сцены, концовки
- словари (`common_names`, `title_words`, `intents`)

Чтобы расширять игру, добавляйте новые записи в JSON-файлы без изменения движка.

## Тесты
```bash
pytest
```
