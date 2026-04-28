<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MovieSubmissionForm
from django.contrib.auth.decorators import login_required
from movies.models import Movie, UserMovie
from movies.tmdb import get_movie
=======
from django.shortcuts import render, redirect
from .forms import MovieSubmissionForm
from django.contrib.auth.decorators import login_required
from movies.models import Movie
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f


@login_required
def submit_movie(request):
    if request.method == 'POST':
<<<<<<< HEAD
        form = MovieSubmissionForm(request.POST)
=======
        form = MovieSubmissionForm(request.POST, request.FILES)
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            return redirect('home')
    else:
        form = MovieSubmissionForm()

<<<<<<< HEAD
    return render(request, 'submissions/form.html', {'form': form})


@login_required
def upload_movie(request):
    """Загрузка фильма через TMDB ID"""
    movie_data = None
    error = None
    
    if request.method == 'POST':
        tmdb_id = request.POST.get('tmdb_id')
        if tmdb_id:
            try:
                data = get_movie(int(tmdb_id))
                if data and 'title' in data:
                    movie_data = data
                    # Сохраняем фильм в базу
                    movie, _ = Movie.objects.get_or_create(
                        tmdb_id=int(tmdb_id),
                        defaults={
                            'title': data['title'],
                            'description': data.get('overview', ''),
                            'year': data.get('release_date', '')[:4] or None,
                            'poster': f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}",
                            'source': 'tmdb'
                        }
                    )
                    # Добавляем в коллекцию пользователя
                    UserMovie.objects.get_or_create(
                        user=request.user,
                        movie=movie,
                        defaults={'status': 'planned'}
                    )
                    return redirect('profile')
                else:
                    error = 'Фильм не найден'
            except (ValueError, Exception) as e:
                error = f'Ошибка: {str(e)}'
    
    return render(request, 'submissions/upload_movie.html', {
        'movie_data': movie_data,
        'error': error,
    })
=======
    return render(request, 'submissions/upload_movie.html', {'form': form})
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f


@login_required
def profile_view(request):
<<<<<<< HEAD
    """Профиль пользователя с его фильмами"""
    user_movies = UserMovie.objects.filter(user=request.user).select_related('movie')
    
    context = {
        'user_movies': user_movies,
    }
    return render(request, 'submissions/profile.html', context)
=======
    """Страница профиля пользователя"""
    movies = Movie.objects.filter(usermovie__user=request.user).select_related('usermovie')
    
    context = {
        'movies': movies,
        'favorites': [],  # Можно добавить функционал избранного
    }
    
    return render(request, 'movies/profile.html', context)
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f
