from django.urls import path
<<<<<<< HEAD
from .views import submit_movie, upload_movie, profile_view
from .views_auth import register_view, CustomLoginView

urlpatterns = [
    path('submit/', submit_movie, name='submit_movie'),
    path('upload/', upload_movie, name='upload_movie'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
=======
from .views import submit_movie, profile_view

urlpatterns = [
    path('submit/', submit_movie, name='submit_movie'),
    path('upload/', submit_movie, name='upload_movie'),
    path('profile/', profile_view, name='profile'),
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f
]