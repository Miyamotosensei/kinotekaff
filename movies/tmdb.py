import requests
from django.conf import settings


def search_movies(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": query,
        "language": "ru-RU"
    }
    return requests.get(url, params=params).json()


def get_movie(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ru-RU"
    }
    return requests.get(url, params=params).json()