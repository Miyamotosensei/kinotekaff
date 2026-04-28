from django.contrib import admin
from .models import MovieSubmission
from movies.models import Movie


@admin.action(description="Одобрить фильмы")
def approve_movies(modeladmin, request, queryset):
    for sub in queryset:
        Movie.objects.create(
            title=sub.title,
            description=sub.description,
            year=sub.year,
            poster=sub.poster,
            source='user'
        )
        sub.status = 'approved'
        sub.save()


@admin.register(MovieSubmission)
class MovieSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    actions = [approve_movies]