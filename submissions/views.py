from django.shortcuts import render, redirect
from .forms import MovieSubmissionForm
from django.contrib.auth.decorators import login_required
from movies.models import Movie


@login_required
def submit_movie(request):
    if request.method == 'POST':
        form = MovieSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            return redirect('home')
    else:
        form = MovieSubmissionForm()

    return render(request, 'submissions/upload_movie.html', {'form': form})


@login_required
def profile_view(request):
    """Страница профиля пользователя"""
    movies = Movie.objects.filter(usermovie__user=request.user).select_related('usermovie')
    
    context = {
        'movies': movies,
        'favorites': [],  # Можно добавить функционал избранного
    }
    
    return render(request, 'movies/profile.html', context)