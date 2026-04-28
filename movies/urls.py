from django.urls import path
from .views import (
    home, search_view, import_movie, movie_detail, add_movie, 
    movie_detail_tmdb, delete_comment
)

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_view, name='search'),
    path('import/<int:tmdb_id>/', import_movie, name='import_movie'),
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),
    path('movie/<int:pk>/slug/<slug:slug>/', movie_detail, name='movie_detail_slug'),
    path('tmdb/<int:tmdb_id>/', movie_detail_tmdb, name='movie_detail_tmdb'),
    path('add/', add_movie, name='add_movie'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]