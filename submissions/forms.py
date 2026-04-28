from django import forms
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
=======
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f
from .models import MovieSubmission


class MovieSubmissionForm(forms.ModelForm):
    class Meta:
        model = MovieSubmission
<<<<<<< HEAD
        fields = ['title', 'description', 'year', 'poster']


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-gray-800 text-white placeholder-gray-500 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-kino-accent border border-gray-700 transition-all',
            'placeholder': 'your@email.com'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full bg-gray-800 text-white placeholder-gray-500 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-kino-accent border border-gray-700 transition-all',
                'placeholder': 'Придумайте имя пользователя',
                'autocomplete': 'username',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full bg-gray-800 text-white placeholder-gray-500 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-kino-accent border border-gray-700 transition-all',
                'placeholder': 'Придумайте надёжный пароль',
                'autocomplete': 'new-password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full bg-gray-800 text-white placeholder-gray-500 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-kino-accent border border-gray-700 transition-all',
                'placeholder': 'Повторите пароль',
                'autocomplete': 'new-password',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем стандартные helptexts для cleaner look
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
=======
        fields = ['title', 'description', 'year', 'poster']
>>>>>>> 18c90f6d917a2e6eac59033df41c131b5f5dfd4f
