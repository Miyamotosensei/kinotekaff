from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Avg
from .tmdb import search_movies, get_movie, get_popular_movies, get_movie_videos, search_by_genre, get_genres
from .models import Movie, UserMovie, Comment, Rating
from .forms import CommentForm, RatingForm, MovieUploadForm


def home(request):
    """Главная страница с популярными фильмами"""
    # Получаем локальные фильмы
    movies = Movie.objects.all()
    tmdb_movies = []
    
    # Фильтрация по жанру
    genre = request.GET.get('genre')
    if genre:
        movies = movies.filter(genre=genre)
    
    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    if sort == 'rating':
        movies = sorted(movies, key=lambda m: m.get_average_rating(), reverse=True)
    elif sort == 'title':
        movies = movies.order_by('title')
    else:  # По умолчанию новые
        movies = movies.order_by('-created_at')
    
    # Поиск
    query = request.GET.get('q')
    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(description__icontains=query))
        # Если это поиск, добавляем результаты из TMDB
        tmdb_data = search_movies(query) or {}
        tmdb_results = tmdb_data.get('results', [])[:6]
        movies_list = list(movies)[:12]
        context = {
            'movies': movies_list,
            'tmdb_movies': tmdb_results,
            'query': query,
            'sort': sort,
            'genre': genre,
            'genres': Movie.GENRE_CHOICES,
        }
        return render(request, 'movies/index.html', context)
    
    if not isinstance(movies, list):
        movies = list(movies[:12])
    
    # Если нет локальных фильмов, получаем популярные из TMDB
    if not movies:
        tmdb_data = get_popular_movies()
        if tmdb_data and tmdb_data.get('results'):
            tmdb_movies = tmdb_data.get('results', [])[:12]
    
    context = {
        'movies': movies,
        'tmdb_movies': tmdb_movies,
        'query': query,
        'sort': sort,
        'genre': genre,
        'genres': Movie.GENRE_CHOICES,
    }
    return render(request, 'movies/index.html', context)


def movie_detail_tmdb(request, tmdb_id):
    """Страница TMDB фильма с информацией и трейлером"""
    movie_data = get_movie(tmdb_id)
    
    if not movie_data:
        return redirect('home')
    
    # Получаем трейлер
    trailer_key = get_movie_videos(tmdb_id)
    
    context = {
        'movie': movie_data,
        'trailer_key': trailer_key,
        'is_tmdb': True,
        'tmdb_id': tmdb_id,
    }
    return render(request, 'movies/movie_detail_tmdb.html', context)


def movie_detail(request, pk):
    """Страница фильма с плеером, рейтингом и комментариями"""
    movie = get_object_or_404(Movie, pk=pk)
    comments = movie.comments.all()
    avg_rating = movie.get_average_rating()
    user_rating = None
    
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(movie=movie, user=request.user)
        except Rating.DoesNotExist:
            pass
    
    # Обработка добавления комментария
    comment_form = CommentForm()
    if request.method == 'POST' and 'comment_submit' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': comment.id,
                        'user': comment.user.username,
                        'text': comment.text,
                        'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
                    }
                })
            return redirect('movie_detail', pk=pk)
    
    # Обработка оценки
    rating_form = RatingForm()
    if request.method == 'POST' and 'rating_submit' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating_value = rating_form.cleaned_data['rating']
            rating, created = Rating.objects.update_or_create(
                movie=movie,
                user=request.user,
                defaults={'rating': rating_value}
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'rating': rating_value,
                    'avg_rating': movie.get_average_rating(),
                    'rating_count': movie.get_rating_count()
                })
            return redirect('movie_detail', pk=pk)
    
    context = {
        'movie': movie,
        'comments': comments,
        'avg_rating': avg_rating,
        'rating_count': movie.get_rating_count(),
        'user_rating': user_rating,
        'comment_form': comment_form,
        'rating_form': rating_form,
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required(login_url='login')
def add_movie(request):
    """Форма для загрузки фильма пользователем"""
    if request.method == 'POST':
        form = MovieUploadForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            movie.source = 'user'
            movie.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieUploadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'movies/add_movie.html', context)


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
