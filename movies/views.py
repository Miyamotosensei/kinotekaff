from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from .tmdb import search_movies, get_movie, get_popular_movies, get_movie_videos, search_by_genre, get_genres
from .models import Movie, UserMovie, Comment, Rating, Genre
from .forms import CommentForm, RatingForm, MovieUploadForm


def home(request):
    """Главная страница с фильтрацией и сортировкой"""
    # Получаем все фильмы с оптимизацией
    movies = Movie.objects.select_related('author').prefetch_related('genres').all()
    
    # Фильтрация по жанру
    genre = request.GET.get('genre')
    if genre:
        try:
            genre_obj = Genre.objects.get(slug=genre)
            movies = movies.filter(genres=genre_obj)
        except Genre.DoesNotExist:
            pass
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        movies = movies.filter(category=category)
    
    # Фильтрация по году
    year = request.GET.get('year')
    if year:
        movies = movies.filter(year=year)
    
    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    if sort == 'rating':
        # Сортировка по рейтингу через аннотацию
        movies = movies.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')
    elif sort == 'title':
        movies = movies.order_by('title')
    elif sort == 'year':
        movies = movies.order_by('-year')
    elif sort == 'views':
        movies = movies.order_by('-views_count')
    else:  # По умолчанию новые
        movies = movies.order_by('-created_at')
    
    # Поиск
    query = request.GET.get('q')
    if query:
        movies = movies.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        # Если это поиск, добавляем результаты из TMDB
        tmdb_data = search_movies(query) or {}
        tmdb_results = tmdb_data.get('results', [])[:6]
    else:
        tmdb_results = []
    
    # Пагинация
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page', 1)
    movies_page = paginator.get_page(page_number)
    
    # Получаем жанры для фильтра
    genres = Genre.objects.all()
    
    # Получаем годы для фильтра
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Hero movie - первый фильм для главного баннера
    hero_movie = movies_page[0] if movies_page else None
    
    context = {
        'movies': movies_page,
        'tmdb_movies': tmdb_results,
        'query': query,
        'sort': sort,
        'genre': genre,
        'category': category,
        'year': year,
        'genres': genres,
        'years': years,
        'hero_movie': hero_movie,
    }
    return render(request, 'movies/index.html', context)


def movie_detail_tmdb(request, tmdb_id):
    """Страница TMDB фильма с информацией и трейлером"""
    movie_data = get_movie(tmdb_id)
    
    if not movie_data:
        return redirect('home')
    
    # Получаем трейлер
    trailer_key = get_movie_videos(tmdb_id)
    
    # Получаем похожие фильмы из TMDB
    similar_movies = []
    # Можно добавить вызов API для похожих фильмов
    
    context = {
        'movie': movie_data,
        'trailer_key': trailer_key,
        'is_tmdb': True,
        'tmdb_id': tmdb_id,
        'similar_movies': similar_movies,
    }
    return render(request, 'movies/movie_detail_tmdb.html', context)


def movie_detail(request, pk):
    """Страница фильма с плеером, рейтингом и комментариями"""
    movie = get_object_or_404(
        Movie.objects.select_related('author').prefetch_related('genres', 'comments__user'),
        pk=pk
    )
    
    # Увеличиваем счетчик просмотров
    movie.views_count += 1
    movie.save(update_fields=['views_count'])
    
    # Комментарии с оптимизацией
    comments = movie.comments.select_related('user').order_by('-created_at')[:50]
    
    avg_rating = movie.get_average_rating()
    user_rating = None
    
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(movie=movie, user=request.user)
        except Rating.DoesNotExist:
            pass
    
    # Похожие фильмы
    similar_movies = movie.get_similar_movies(limit=6)
    
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
        'similar_movies': similar_movies,
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required(login_url='login')
def upload_movie(request):
    """Форма для загрузки фильма пользователем (алиас для add_movie)"""
    if request.method == 'POST':
        form = MovieUploadForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            movie.source = 'user'
            movie.is_user_uploaded = True
            movie.save()
            form.save_m2m()  # Сохраняем многие-ко-многим (жанры)
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieUploadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'movies/upload_movie.html', context)


@login_required(login_url='login')
def add_movie(request):
    """Форма для загрузки фильма пользователем"""
    if request.method == 'POST':
        form = MovieUploadForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            movie.source = 'user'
            movie.is_user_uploaded = True
            movie.save()
            form.save_m2m()  # Сохраняем многие-ко-многим (жанры)
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieUploadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'movies/add_movie.html', context)


def search_view(request):
    """Поиск фильмов с результатами из локальной БД и TMDB"""
    query = request.GET.get('q', '')
    local_results = []
    tmdb_results = []

    if query:
        # Локальный поиск
        local_results = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).select_related('author').prefetch_related('genres')[:12]
        
        # Поиск в TMDB
        data = search_movies(query)
        if data:
            tmdb_results = data.get('results', [])[:12]

    context = {
        'query': query,
        'local_results': local_results,
        'tmdb_results': tmdb_results,
    }
    return render(request, 'movies/search.html', context)


def import_movie(request, tmdb_id):
    """Импорт фильма из TMDB в локальную базу"""
    data = get_movie(tmdb_id)
    
    if not data:
        return redirect('home')

    # Получаем или создаем жанры
    genre_objects = []
    for genre_data in data.get('genres', []):
        genre_name = genre_data.get('name', '')
        if genre_name:
            slug = genre_name.lower().replace(' ', '-').replace('-', '')
            genre, _ = Genre.objects.get_or_create(
                slug=slug,
                defaults={'name': genre_name}
            )
            genre_objects.append(genre)

    movie, created = Movie.objects.get_or_create(
        tmdb_id=tmdb_id,
        defaults={
            'title': data['title'],
            'description': data.get('overview', ''),
            'year': data.get('release_date', '')[:4] or None,
            'poster': f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get('poster_path') else None,
            'source': 'tmdb',
            'category': 'movie',
        }
    )
    
    # Добавляем жанры
    if genre_objects:
        movie.genres.set(genre_objects)

    if request.user.is_authenticated:
        UserMovie.objects.get_or_create(
            user=request.user,
            movie=movie,
            defaults={'status': 'planned'}
        )

    return redirect('movie_detail', pk=movie.pk)


@login_required
def delete_comment(request, comment_id):
    """Удаление комментария (только автором)"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user == request.user:
        movie_pk = comment.movie.pk
        comment.delete()
        return redirect('movie_detail', pk=movie_pk)
    
    return redirect('home')
