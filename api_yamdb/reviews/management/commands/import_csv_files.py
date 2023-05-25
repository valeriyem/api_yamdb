from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Genre, Title

ALREDY_LOADED_ERROR_MESSAGE = """
Ошибка загрузки из csv файлов!
1) Удалить db.sqlite3
2) Выполнить миграции
3) Выполнить загрузку информации из csv
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Title.objects.exists():
            print('Модель Title уже существует в таблице!')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        elif Category.objects.exists():
            print('Модель Category уже существует в таблице!')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        elif Genre.objects.exists():
            print('Модель Genre уже существует в таблице!')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        else:
            pass

        print('Загрузка информации из csv файлов в базу данных.')

        for row in DictReader(
            open('static/data/category.csv', encoding='utf-8')
        ):
            category = Category(
                name=row['name'],
                slug=row['slug'],
            )
            category.save()

        for row in DictReader(open('static/data/genre.csv', encoding='utf-8')):
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
