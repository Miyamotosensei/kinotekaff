"""
Скрипт для автоматического импорта популярных фильмов из TMDB.
Запускается при первом запуске проекта для заполнения базы данных.

Использование:
    python manage.py shell < movies/management/commands/import_popular_movies.py
    
Или через management command:
    python manage.py import_popular_movies
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.base import ContentFile
import requests
from django.conf import settings
from movies.models import Movie, Genre


def get_genres_from_tmdb():
    """Получить список жанров из TMDB и создать их в БД"""
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            tmdb_genres = response.json().get('genres', [])
            
            for tmdb_genre in tmdb_genres:
                genre, created = Genre.objects.get_or_create(
                    name=tmdb_genre['name'],
                    defaults={'slug': tmdb_genre['name'].lower().replace(' ', '-')}
                )
                # Сохраняем TMDB ID жанра в поле, если нужно
                if not hasattr(genre, 'tmdb_id'):
                    genre.tmdb_id = tmdb_genre['id']
                    genre.save()
                    
            print(f"✅ Импортировано {len(tmdb_genres)} жанров из TMDB")
            return tmdb_genres
    except Exception as e:
        print(f"❌ Ошибка при получении жанров: {e}")
    
    return []


def download_poster(poster_url):
    """Скачать постер фильма и вернуть как ContentFile"""
    if not poster_url:
        return None
    
    try:
        response = requests.get(poster_url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content)
    except Exception as e:
        print(f"⚠️ Ошибка при скачивании постера: {e}")
    
    return None


def import_popular_movies(count=20):
    """Импортировать популярные фильмы из TMDB"""
    print("🎬 Начинаем импорт популярных фильмов из TMDB...")
    
    # Сначала получаем и создаем жанры
    tmdb_genres = get_genres_from_tmdb()
    if not tmdb_genres:
        print("⚠️ Не удалось получить жанры, продолжаем без них...")
    
    # Получаем популярные фильмы
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU",
        "page": 1,
        "region": "RU"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            print(f"❌ Ошибка API TMDB: {response.status_code}")
            return 0
            
        data = response.json()
        movies_data = data.get('results', [])[:count]
        
        imported_count = 0
        skipped_count = 0
        
        for movie_data in movies_data:
            tmdb_id = movie_data.get('id')
            
            # Проверяем, есть ли уже такой фильм в базе
            if Movie.objects.filter(tmdb_id=tmdb_id).exists():
                print(f"⏭️ Фильм '{movie_data.get('title')}' уже существует, пропускаем...")
                skipped_count += 1
                continue
            
            # Создаем объект фильма
            title = movie_data.get('title') or movie_data.get('original_title', 'Без названия')
            description = movie_data.get('overview', '')
            year = None
            release_date = movie_data.get('release_date')
            if release_date:
                year = int(release_date.split('-')[0])
            
            poster_url = None
            if movie_data.get('poster_path'):
                poster_url = f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}"
            
            # Определяем качество на основе популярности (условно)
            popularity = movie_data.get('popularity', 0)
            if popularity > 200:
                quality = '4K'
            elif popularity > 100:
                quality = 'FullHD'
            else:
                quality = 'HD'
            
            movie = Movie(
                title=title,
                description=description[:2000] if description else '',  # Ограничиваем длину
                year=year,
                poster=poster_url,
                source='tmdb',
                tmdb_id=tmdb_id,
                quality=quality,
                views_count=0,
            )
            
            # Скачиваем и сохраняем постер
            if poster_url:
                poster_content = download_poster(poster_url)
                if poster_content:
                    filename = f"poster_{tmdb_id}.jpg"
                    movie.poster_file.save(filename, poster_content, save=False)
            
            movie.save()
            
            # Добавляем жанры
            tmdb_genre_ids = movie_data.get('genre_ids', [])
            if tmdb_genre_ids and tmdb_genres:
                for tmdb_genre in tmdb_genres:
                    if tmdb_genre['id'] in tmdb_genre_ids:
                        try:
                            genre = Genre.objects.get(name=tmdb_genre['name'])
                            movie.genres.add(genre)
                        except Genre.DoesNotExist:
                            pass
            
            movie.save()
            imported_count += 1
            print(f"✅ Добавлен фильм: {title} ({year}) - Рейтинг: {movie_data.get('vote_average', 0):.1f}")
        
        print(f"\n🎉 Импорт завершен!")
        print(f"   ✅ Добавлено фильмов: {imported_count}")
        print(f"   ⏭️ Пропущено (уже существуют): {skipped_count}")
        print(f"   📊 Всего в базе: {Movie.objects.count()}")
        
        return imported_count
        
    except Exception as e:
        print(f"❌ Критическая ошибка при импорте: {e}")
        return 0


if __name__ == '__main__':
    # Запуск импорта
    count = import_popular_movies(count=20)
    
    if count > 0:
        print("\n✨ Главная страница больше не пустая! Можно запускать сервер.")
    else:
        print("\n⚠️ Импорт не выполнен или фильмы уже существуют в базе.")
