from django.shortcuts import render, redirect, get_object_or_404
from .tmdb import search_movies, get_movie
from .models import Movie, UserMovie


def home(request):
    """Главная страница с популярными фильмами"""
    # Получаем популярные фильмы из TMDB
    data = search_movies('popular') or {}
    results = data.get('results', [])[:12]  # Берем первые 12 фильмов
    
    # Если есть запрос поиска, обрабатываем его
    query = request.GET.get('q')
    if query and query != 'popular':
        data = search_movies(query)
        results = data.get('results', [])[:12] if data else []
    
    context = {
        'movies': results,
        'query': query,
    }
    return render(request, 'movies/index.html', context)


def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        data = search_movies(query)
        results = data.get('results', [])

    return render(request, 'movies/search.html', {'results': results})


def import_movie(request, tmdb_id):
    data = get_movie(tmdb_id)

    movie, _ = Movie.objects.get_or_create(
        tmdb_id=tmdb_id,
        defaults={
            'title': data['title'],
            'description': data.get('overview', ''),
            'year': data.get('release_date', '')[:4] or None,
            'poster': f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}",
            'source': 'tmdb'
        }
    )

    if request.user.is_authenticated:
        UserMovie.objects.get_or_create(
            user=request.user,
            movie=movie,
            defaults={'status': 'planned'}
        )

    return redirect('home')