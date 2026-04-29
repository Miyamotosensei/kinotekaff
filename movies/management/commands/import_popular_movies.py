"""
Management command для импорта популярных фильмов из TMDB.

Использование:
    python manage.py import_popular_movies [--count N]
    
Аргументы:
    --count, -c  Количество фильмов для импорта (по умолчанию 20)
"""

from django.core.management.base import BaseCommand
from movies.import_popular_movies import import_popular_movies


class Command(BaseCommand):
    help = 'Импортирует популярные фильмы из TMDB для заполнения базы данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', '-c',
            type=int,
            default=20,
            help='Количество фильмов для импорта (по умолчанию 20)'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(f'🎬 Запуск импорта {count} популярных фильмов из TMDB...')
        
        imported = import_popular_movies(count=count)
        
        if imported > 0:
            self.stdout.write(self.style.SUCCESS(f'\n✨ Успешно импортировано {imported} фильмов!'))
            self.stdout.write(self.style.SUCCESS('Главная страница больше не пустая!'))
        else:
            self.stdout.write(self.style.WARNING('\n⚠️ Импорт не выполнен или фильмы уже существуют в базе.'))
