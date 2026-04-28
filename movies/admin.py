from django.contrib import admin
<<<<<<< HEAD
from .models import Movie, Comment, Rating, UserMovie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'source', 'author', 'created_at', 'get_rating_count')
    list_filter = ('genre', 'source', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'get_average_rating', 'get_rating_count')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'year', 'genre')
        }),
        ('Изображения и видео', {
            'fields': ('poster', 'poster_file', 'video_file')
        }),
        ('Метаданные', {
            'fields': ('author', 'source', 'tmdb_id')
        }),
        ('Статистика', {
            'fields': ('get_average_rating', 'get_rating_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    list_filter = ('created_at', 'movie')
    search_fields = ('text', 'user__username', 'movie__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'movie')
    search_fields = ('user__username', 'movie__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserMovie)
class UserMovieAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'movie__title')
=======

# Register your models here.
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f
