from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment, GenreTitle
from users.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
Ошибка загрузки из csv файлов!
1) Удалить db.sqlite3
2) Выполнить миграции
3) Выполнить загрузку информации из csv
"""


class Command(BaseCommand):
    def handle(self, *args, **options):

        print('Загрузка информации из csv файлов в базу данных.')

        for row in DictReader(
                open('static/data/users.csv', encoding='utf-8')
        ):
            users = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            users.save()

        for row in DictReader(
                open('static/data/category.csv', encoding='utf-8')
        ):
            category = Category(
                name=row['name'],
                slug=row['slug'],
            )
            category.save()

        for row in DictReader(
                open('static/data/genre.csv', encoding='utf-8')
        ):
            genre = Genre(
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

        for row in DictReader(
                open('static/data/titles.csv', encoding='utf-8')
        ):
            category = Category.objects.get(
                id=row['category'],
            )
            title = Title(
                name=row['name'],
                year=row['year'],
                category=category,
            )
            title.save()

        for row in DictReader(
                open('static/data/genre_title.csv', encoding='utf-8')
        ):
            title_id = Title.objects.get(id=row['title_id'])
            genre_id = Genre.objects.get(id=row['genre_id'])

            genre_title = GenreTitle(
                title=title_id,
                genre=genre_id,
            )
            genre_title.save()

        for row in DictReader(
                open('static/data/review.csv', encoding='utf-8')
        ):
            author_id = User.objects.get(id=row['author'])

            review = Review(
                title_id=row['title_id'],
                text=row['text'],
                author=author_id,
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        for row in DictReader(
                open('static/data/comments.csv', encoding='utf-8')
        ):
            author_id = User.objects.get(id=row['author'])
            review_id = Review.objects.get(id=row['review_id'])

            comments = Comment(
                review=review_id,
                text=row['text'],
                author=author_id,
                pub_date=row['pub_date'],
            )
            comments.save()

        print('Загрузка прошла успешно!')
