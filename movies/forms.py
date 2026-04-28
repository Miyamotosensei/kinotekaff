from django import forms
from .models import Comment, Rating, Movie


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-kino-accent resize-none',
                'placeholder': 'Напишите ваш комментарий...',
                'rows': 4
            })
        }
        labels = {
            'text': 'Комментарий'
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-white focus:outline-none focus:border-kino-accent'
            })
        }
        labels = {
            'rating': 'Ваша оценка'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.choices = [(i, f'{"⭐" * i} ({i}/10)') for i in range(1, 11)]


class MovieUploadForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'year', 'poster_file', 'video_file', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-kino-accent',
                'placeholder': 'Название фильма'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-kino-accent resize-none',
                'placeholder': 'Описание фильма',
                'rows': 5
            }),
            'genre': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-white focus:outline-none focus:border-kino-accent'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-kino-accent',
                'placeholder': 'Год выпуска'
            }),
            'poster_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-gray-400 focus:outline-none focus:border-kino-accent',
                'accept': 'image/*'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-gray-400 focus:outline-none focus:border-kino-accent',
                'accept': 'video/*'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-kino-card border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-kino-accent',
                'placeholder': 'URL видео (например, https://www.youtube.com/embed/...)'
            })
        }
        labels = {
            'title': 'Название фильма',
            'description': 'Описание',
            'genre': 'Жанр',
            'year': 'Год выпуска',
            'poster_file': 'Постер фильма',
            'video_file': 'Видеофайл',
            'video_url': 'URL видео (iframe)'
        }
