from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Movie(models.Model):
    SOURCE_CHOICES = [
        ('tmdb', 'TMDb'),
        ('user', 'User'),
    ]

    CATEGORY_CHOICES = [
        ('movie', 'Фильм'),
        ('series', 'Сериал'),
        ('cartoon', 'Мультфильм'),
    ]

    GENRE_CHOICES = [
        ('action', 'Экшен'),
        ('comedy', 'Комедия'),
        ('drama', 'Драма'),
        ('horror', 'Ужас'),
        ('thriller', 'Триллер'),
        ('sci-fi', 'Научная фантастика'),
        ('romance', 'Романтика'),
        ('adventure', 'Приключения'),
        ('animation', 'Мультфильм'),
        ('documentary', 'Документальный'),
        ('fantasy', 'Фэнтези'),
        ('crime', 'Криминал'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField(null=True, blank=True)
    poster = models.URLField(blank=True, null=True)
    poster_file = models.ImageField(upload_to='posters/', null=True, blank=True)
    
    # Категория (Фильм, Сериал, Мультфильм)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='movie')
    
    # Жанры (многие-ко-многим)
    genres = models.ManyToManyField('Genre', blank=True, related_name='movies')
    
    # Поле для загрузки видеофайла
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    
    # iframe URL для сторонних плееров
    iframe_url = models.URLField(blank=True, null=True, help_text="URL для встраивания плеера (например, с videocdn.tv)")
    
    # Автор фильма (пользователь, который загрузил)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')

    tmdb_id = models.IntegerField(null=True, blank=True, unique=True)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    
    # Дополнительные поля для статистики
    views_count = models.PositiveIntegerField(default=0)
    quality = models.CharField(max_length=10, blank=True, null=True, help_text="Качество видео (HD, FullHD, 4K)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['year']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        """Получить среднюю оценку фильма"""
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    
    def get_rating_count(self):
        """Получить количество оценок"""
        return self.ratings.count()
    
    def get_similar_movies(self, limit=6):
        """Получить похожие фильмы по жанрам"""
        if self.genres.exists():
            genre_ids = self.genres.values_list('id', flat=True)
            similar = Movie.objects.filter(
                genres__in=genre_ids
            ).exclude(
                id=self.id
            ).distinct().select_related('author').prefetch_related('genres')[:limit]
            if similar.exists():
                return similar
        
        # Если нет жанров, возвращаем последние добавленные
        return Movie.objects.exclude(id=self.id).select_related('author').prefetch_related('genres')[:limit]


class Genre(models.Model):
    """Модель жанров для гибкой системы категорий"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['movie', '-created_at']),
        ]

    def __str__(self):
        return f"Комментарий {self.user.username} к {self.movie.title}"


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'user')  # Один пользователь - одна оценка на фильм
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['movie', 'user']),
        ]

    def __str__(self):
        return f"{self.user.username} оценил {self.movie.title} на {self.rating}"


class UserMovie(models.Model):
    STATUS = [
        ('planned', 'Буду смотреть'),
        ('watched', 'Просмотрено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS)

    class Meta:
        unique_together = ('user', 'movie')
        indexes = [
            models.Index(fields=['user', 'status']),
        ]