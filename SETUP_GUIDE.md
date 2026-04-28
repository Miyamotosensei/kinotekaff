# Настройка проекта «Кинотека»

## ✅ Выполненные изменения в settings.py

### 1. WhiteNoise для раздачи статики
- Добавлен `whitenoise.runserver_nostatic` в `INSTALLED_APPS`
- Добавлен `whitenoise.middleware.WhiteNoiseMiddleware` в `MIDDLEWARE`
- Настроен `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
- Создана директория `static/` и добавлена в `STATICFILES_DIRS`

### 2. CSRF_TRUSTED_ORIGINS
Добавлен ваш домен в список доверенных источников:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://kinotekaff-production.up.railway.app',
    'http://localhost',
    'http://127.0.0.1',
]
```

## 🎬 Автоматический импорт фильмов из TMDB

### Способ 1: Management Command (рекомендуется)
```bash
python manage.py import_popular_movies --count 20
```

**Параметры:**
- `--count N` или `-c N` — количество фильмов для импорта (по умолчанию 20)

### Способ 2: Прямой запуск скрипта
```bash
python movies/import_popular_movies.py
```

### Что делает скрипт:
1. ✅ Получает список жанров из TMDB и создает их в БД
2. ✅ Загружает популярные фильмы из TMDB API
3. ✅ Скачивает постеры фильмов и сохраняет их локально
4. ✅ Создает записи в базе данных с полной информацией
5. ✅ Привязывает жанры к фильмам
6. ✅ Определяет качество видео на основе популярности (HD/FullHD/4K)

## 📊 Результаты импорта

После запуска импорта:
- **15 популярных фильмов** добавлено в базу
- **19 жанров** создано автоматически
- Все фильмы имеют постеры, описания, год выпуска
- Жанры привязаны к фильмам для работы фильтров

## 🚀 Быстрый старт

```bash
# 1. Применить миграции
python manage.py migrate

# 2. Импортировать популярные фильмы
python manage.py import_popular_movies --count 20

# 3. Собрать статику для production (опционально)
python manage.py collectstatic --noinput

# 4. Запустить сервер
python manage.py runserver
```

## 📁 Структура файлов

```
/workspace/
├── config/
│   └── settings.py          # Настройки Django + WhiteNoise + CSRF
├── movies/
│   ├── import_popular_movies.py              # Скрипт импорта
│   └── management/
│       └── commands/
│           └── import_popular_movies.py      # Management command
├── static/                    # Директория для статики
├── media/                     # Директория для медиафайлов
└── staticfiles/               # Собранные статические файлы
```

## 🔧 Дополнительные настройки

### Для production (Railway.app):
Убедитесь, что в настройках Railway добавлены переменные окружения:
- `SECRET_KEY` — секретный ключ Django
- `TMDB_API_KEY` — ваш API ключ TMDB
- `DEBUG=False` — для production режима

### Если нужно изменить количество импортируемых фильмов:
```bash
# Импортировать 50 фильмов
python manage.py import_popular_movies --count 50

# Импортировать 100 фильмов (5 страниц по 20)
python manage.py shell -c "from movies.import_popular_movies import import_popular_movies; import_popular_movies(100)"
```

## ⚠️ Важно

- Скрипт проверяет наличие фильма по `tmdb_id` и не дублирует записи
- Постеры скачиваются и сохраняются в `media/posters/`
- Для работы требуется установленная библиотека `requests` (уже установлена)
- API ключ TMDB уже настроен в settings.py
