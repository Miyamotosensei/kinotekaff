from django.db import models
from django.contrib.auth.models import User


class MovieSubmission(models.Model):
    STATUS = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    poster = models.URLField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    moderator_comment = models.TextField(blank=True)