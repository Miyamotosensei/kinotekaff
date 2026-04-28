from django.urls import path
from .views import home, search_view, import_movie, movie_detail, add_movie

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_view, name='search'),
    path('import/<int:tmdb_id>/', import_movie, name='import_movie'),
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),
    path('add/', add_movie, name='add_movie'),
]