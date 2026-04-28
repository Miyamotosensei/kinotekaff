from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Movie(models.Model):
    SOURCE_CHOICES = [
        ('tmdb', 'TMDb'),
        ('user', 'User'),
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
    
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True, blank=True)
    
    # Поле для загрузки видеофайла
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    
    # Поле для URL видео (iframe)
    video_url = models.URLField(blank=True, null=True, help_text="URL для вставки видео через iframe")
    
    # Автор фильма (пользователь, который загрузил)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')

    tmdb_id = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        """Получить среднюю оценку фильма"""
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    
    def get_rating_count(self):
        """Получить количество оценок"""
        return self.ratings.count()


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

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