"""
Темплейтеги для проекта Кинотека
"""
from django import template

register = template.Library()


@register.filter
def tmdb_image_url(poster_path, size='w500'):
    """
    Формирует полный URL для постера TMDB.
    
    Использование в шаблоне:
    {{ movie.poster_path|tmdb_image_url }}
    {{ movie.poster_path|tmdb_image_url:'w780' }}
    
    Доступные размеры: w92, w154, w185, w342, w500, w780, original
    """
    if not poster_path:
        return 'https://via.placeholder.com/500x750?text=No+Poster'
    
    base_url = 'https://image.tmdb.org/t/p/'
    return f'{base_url}{size}{poster_path}'


@register.filter
def tmdb_backdrop_url(backdrop_path, size='original'):
    """
    Формирует полный URL для фонового изображения TMDB.
    
    Использование в шаблоне:
    {{ movie.backdrop_path|tmdb_backdrop_url }}
    
    Доступные размеры: w300, w780, w1280, original
    """
    if not backdrop_path:
        return ''
    
    base_url = 'https://image.tmdb.org/t/p/'
    return f'{base_url}{size}{backdrop_path}'


@register.filter
def get_year(date_string):
    """
    Извлекает год из строки даты (формат TMDB: YYYY-MM-DD).
    
    Использование в шаблоне:
    {{ movie.release_date|get_year }}
    """
    if not date_string:
        return '—'
    
    try:
        return date_string[:4]
    except (TypeError, IndexError):
        return '—'


@register.filter
def format_rating(rating):
    """
    Форматирует рейтинг TMDB до одного знака после запятой.
    
    Использование в шаблоне:
    {{ movie.vote_average|format_rating }}
    """
    if rating is None:
        return '0.0'
    
    try:
        return f'{float(rating):.1f}'
    except (TypeError, ValueError):
        return '0.0'


@register.simple_tag
def multiply(value, arg):
    """
    Умножает два числа.
    
    Использование в шаблоне:
    {% multiply movie.vote_count 0.1 %}
    """
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0
