from django.urls import path
<<<<<<< HEAD
from .views import home, search_view, import_movie, movie_detail, add_movie
=======
from .views import search_view, import_movie, home
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_view, name='search'),
    path('import/<int:tmdb_id>/', import_movie, name='import_movie'),
<<<<<<< HEAD
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),
    path('add/', add_movie, name='add_movie'),
=======
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f
]