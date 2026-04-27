from django.urls import path
from .views import submit_movie, profile_view

urlpatterns = [
    path('submit/', submit_movie, name='submit_movie'),
    path('upload/', submit_movie, name='upload_movie'),
    path('profile/', profile_view, name='profile'),
]