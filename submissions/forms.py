from django import forms
from .models import MovieSubmission


class MovieSubmissionForm(forms.ModelForm):
    class Meta:
        model = MovieSubmission
        fields = ['title', 'description', 'year', 'poster']