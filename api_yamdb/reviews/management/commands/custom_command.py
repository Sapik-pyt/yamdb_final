import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

CHOISE = {
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    # GenreTitle: "genre_title.csv",
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, file in CHOISE.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{file}',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                model.objects.bulk_create(
                    model(**i) for i in reader)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
