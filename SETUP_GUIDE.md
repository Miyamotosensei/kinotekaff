# 🎬 Кинотека - Setup Guide

## Что было реализовано

Полноценный функционал онлайн-кинотеатра в стиле Кинопоиска с Dark Mode.

### ✅ Модели (models.py)
- **Movie** - Обновленная модель с полями:
  - `video_file` - загрузка видеофайлов
  - `genre` - выбор жанра из предопределённого списка
  - `poster_file` - загрузка постера
  - `author` - связь с пользователем (загруженный контент)
  - `created_at`, `updated_at` - временные метки
  - Методы: `get_average_rating()`, `get_rating_count()`

- **Comment** - Модель комментариев:
  - Связь с Movie и User
  - Текст комментария (max 1000 символов)
  - Временные метки

- **Rating** - Модель оценок:
  - Оценка от 1 до 10
  - Связь с Movie и User
  - **Ограничение**: один пользователь - одна оценка на фильм (`unique_together`)

### ✅ Логика (views.py)
- **home()** - Главная страница с:
  - Фильтрацией по жанрам (?genre=drama)
  - Сортировкой (по новизне, по рейтингу, по названию)
  - Поиском по названию и описанию

- **movie_detail()** - Страница фильма:
  - HTML5 видеоплеер
  - Средний рейтинг и количество оценок
  - Форма для оставления комментария
  - Интерактивная система оценок (1-10 звёзд)
  - Лента комментариев

- **add_movie()** - Загрузка фильма пользователем:
  - Форма с валидацией
  - Загрузка видеофайла и постера
  - Автоматическое сохранение автора

### ✅ Шаблоны (templates/)
- **movie_detail.html** - Современный плеер:
  - HTML5 video tag с controls
  - Информация о фильме (постер, год, жанр, автор)
  - Блок оценок со звездами
  - Форма для комментариев
  - Лента комментариев с временем

- **add_movie.html** - Форма загрузки:
  - Темные поля ввода
  - Drag-and-drop для файлов
  - Оранжевая кнопка "Опубликовать"
  - Информационное сообщение о правах

- **index.html** - Главная с фильтрами:
  - Navbar с фильтрами по жанрам
  - Кнопки сортировки
  - Кнопка "Загрузить фильм" для авторизованных
  - Карточки фильмов с рейтингом
  - Поддержка как локальных, так и TMDB фильмов

### ✅ Маршруты (urls.py)
- `path('', home, name='home')` - Главная
- `path('movie/<int:pk>/', movie_detail, name='movie_detail')` - Просмотр фильма
- `path('add/', add_movie, name='add_movie')` - Загрузка фильма
- `path('search/', search_view, name='search')` - Поиск
- `path('import/<int:tmdb_id>/', import_movie, name='import_movie')` - Импорт из TMDb

### ✅ Стиль и UX
- **Tailwind CSS** с кастомными цветами:
  - Фон: `#141414` (kino-bg)
  - Карточки: `#1f1f1f` (kino-card)
  - Акценты: `#ff6600` (kino-accent)
- Dark Mode по умолчанию
- Все формы содержат `{% csrf_token %}`
- Все формы загрузки имеют `enctype="multipart/form-data"`

---

## 🚀 Инструкции по запуску

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

Это установит:
- Django 6.0.2
- Pillow 10.0.0 (для работы с изображениями)
- requests (для TMDB API)
- И другие зависимости

### 2. Применение миграций

```bash
# Создать миграции для новых моделей
python manage.py makemigrations

# Применить миграции
python manage.py migrate
```

**Важно!** Если у вас уже есть старая база данных, миграции могут потребовать дополнительных действий. В этом случае:
```bash
# Удалить старую БД (осторожно!)
rm db.sqlite3

# Создать новую БД с миграциями
python manage.py migrate
```

### 3. Создание суперпользователя (admin)

```bash
python manage.py createsuperuser
```

Введите:
- Username: (выберите имя)
- Email: (ваш email)
- Password: (надежный пароль)

### 4. Запуск сервера

```bash
python manage.py runserver
```

Откройте браузер и перейдите на:
- **Главная**: http://127.0.0.1:8000/
- **Admin панель**: http://127.0.0.1:8000/admin/

---

## 📁 Структура медиа-файлов

После первой загрузки фильма на сервере появится папка `media/`:
```
media/
├── videos/          # Видеофайлы фильмов
│   └── movie_1.mp4
└── posters/         # Постеры фильмов
    └── poster_1.jpg
```

Убедитесь, что у Django есть права на запись в эту папку.

---

## 🔐 Важные моменты

### CSRF Protection
Все POST-формы содержат `{% csrf_token %}` - это защита от CSRF-атак.

### File Upload Security
- Максимальный размер загружаемого файла можно установить в settings.py:
  ```python
  DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
  FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
  ```

### Поддерживаемые форматы видео
- MP4 (.mp4)
- WebM (.webm)
- Ogg (.ogg)

### Поддерживаемые форматы постеров
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)

---

## 🎨 Кастомизация стилей

Основные цвета находятся в `base.html`:
```javascript
'kino-bg': '#141414',          // Фон
'kino-card': '#1f1f1f',        // Карточки
'kino-accent': '#ff6600',      // Оранжевый акцент
'kino-accent-hover': '#e65c00',// Акцент при наведении
```

Измените эти значения для изменения цветовой схемы.

---

## 🔧 Полезные команды

```bash
# Создать новое приложение
python manage.py startapp app_name

# Проверить код на ошибки
python manage.py check

# Создать резервную копию БД
python manage.py dumpdata > backup.json

# Восстановить БД из резервной копии
python manage.py loaddata backup.json

# Очистить БД (удалить все данные)
python manage.py flush

# Открыть Django shell
python manage.py shell
```

---

## 🐛 Решение проблем

### Ошибка: "No module named 'PIL'"
```bash
pip install Pillow
```

### Ошибка при миграции: "Duplicate key value violates unique constraint"
```bash
python manage.py migrate --fake-initial
```

### Медиа-файлы не отображаются
Убедитесь, что в `settings.py` установлены:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

И проверьте, что `urls.py` содержит:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📊 Примеры использования

### Добавить фильм через Django shell
```python
python manage.py shell

from django.contrib.auth.models import User
from movies.models import Movie

user = User.objects.first()

movie = Movie.objects.create(
    title="Мой фильм",
    description="Описание фильма",
    year=2024,
    genre="drama",
    author=user,
    source="user"
)
```

### Получить среднюю оценку фильма
```python
movie = Movie.objects.first()
avg_rating = movie.get_average_rating()
print(f"Средняя оценка: {avg_rating}/10")
```

### Получить все комментарии к фильму
```python
comments = movie.comments.all()
for comment in comments:
    print(f"{comment.user.username}: {comment.text}")
```

---

## 🚀 Deploy на production

### Важные шаги:
1. Установите `DEBUG = False` в settings.py
2. Добавьте ваш домен в `ALLOWED_HOSTS`
3. Установите надежный `SECRET_KEY`
4. Используйте PostgreSQL вместо SQLite
5. Настройте статические файлы и медиа
6. Используйте gunicorn/uwsgi для запуска
7. Установите SSL сертификат

---

## 📝 API Endpoints (доступные URL)

| Метод | URL | Описание |
|-------|-----|---------|
| GET | `/` | Главная страница |
| GET | `/movie/<id>/` | Страница фильма |
| POST | `/movie/<id>/` | Добавить комментарий/оценку |
| GET | `/add/` | Форма загрузки фильма |
| POST | `/add/` | Загрузить фильм |
| GET | `/search/` | Поиск |
| GET | `/import/<tmdb_id>/` | Импортировать из TMDb |

---

**Приложение готово к использованию!** 🎉

При возникновении вопросов обратитесь к документации Django: https://docs.djangoproject.com/
