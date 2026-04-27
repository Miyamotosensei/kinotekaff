from django.urls import path
from .views import submit_movie

urlpatterns = [
    path('submit/', submit_movie, name='submit_movie'),
]