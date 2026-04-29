from django.contrib import admin
from .models import Movie, Comment, Rating, UserMovie, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'category', 'source', 'author', 'created_at', 'get_rating_count')
    list_filter = ('category', 'genres', 'source', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'get_average_rating', 'get_rating_count')
    
    filter_horizontal = ('genres',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'year', 'category', 'genres')
        }),
        ('Изображения и видео', {
            'fields': ('poster', 'poster_file', 'video_file', 'iframe_url', 'quality')
        }),
        ('Метаданные', {
            'fields': ('author', 'source', 'tmdb_id')
        }),
        ('Статистика', {
            'fields': ('views_count', 'get_average_rating', 'get_rating_count', 'created_at', 'updated_at'),
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
