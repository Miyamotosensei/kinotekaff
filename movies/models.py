from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    SOURCE_CHOICES = [
        ('tmdb', 'TMDb'),
        ('user', 'User'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField(null=True, blank=True)
    poster = models.URLField(blank=True)

    tmdb_id = models.IntegerField(null=True, blank=True)

    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)

    def __str__(self):
        return self.title


class UserMovie(models.Model):
    STATUS = [
        ('planned', 'Буду смотреть'),
        ('watched', 'Просмотрено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS)