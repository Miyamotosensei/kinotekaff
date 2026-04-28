from django.urls import path
from .views import submit_movie, upload_movie, profile_view
from .views_auth import register_view, CustomLoginView

urlpatterns = [
    path('submit/', submit_movie, name='submit_movie'),
    path('upload/', upload_movie, name='upload_movie'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]