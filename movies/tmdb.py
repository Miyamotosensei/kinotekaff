import requests
from django.conf import settings


def get_popular_movies():
    """
    Получить популярные фильмы из TMDB.
    
    Returns:
        dict: Словарь с ключом 'results', содержащим список фильмов
    """
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU",
        "page": 1
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Добавляем полный URL для постеров в каждый фильм
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            return data
    except requests.exceptions.RequestException:
        pass
    return {"results": []}


def search_movies(query):
    """
    Поиск фильмов по названию в TMDB.
    
    Args:
        query: Строка поискового запроса
        
    Returns:
        dict: Словарь с ключом 'results', содержащим список фильмов
    """
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": query,
        "language": "ru-RU"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Добавляем полный URL для постеров в каждый фильм
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            return data
    except requests.exceptions.RequestException:
        pass
    return {"results": []}


def get_movie(tmdb_id):
    """
    Получить полную информацию о фильме из TMDB.
    
    Args:
        tmdb_id: ID фильма в базе TMDB
        
    Returns:
        dict: Данные о фильме или пустой словарь при ошибке
    """
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Добавляем полный URL для постера прямо в данные
            if data.get('poster_path'):
                data['poster_url'] = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            if data.get('backdrop_path'):
                data['backdrop_url'] = f"https://image.tmdb.org/t/p/original{data['backdrop_path']}"
            return data
    except requests.exceptions.RequestException:
        pass
    return {}


def get_movie_videos(tmdb_id):
    """Получить видео фильма (трейлеры)"""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            # Ищем трейлер на YouTube
            for video in results:
                if video.get('site') == 'YouTube' and video.get('type') in ['Trailer', 'Teaser']:
                    return video.get('key')
    except requests.exceptions.RequestException:
        pass
    return None


def get_genres():
    """Получить список жанров из TMDB"""
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('genres', [])
    except requests.exceptions.RequestException:
        pass
    return []


def search_by_genre(genre_id, page=1):
    """Поиск фильмов по жанру"""
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU",
        "with_genres": genre_id,
        "page": page,
        "sort_by": "popularity.desc"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return {"results": []}