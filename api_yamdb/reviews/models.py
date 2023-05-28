from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User

from .validators import year_validator


class Title(models.Model):
    """Модель для создания произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.SmallIntegerField(
        validators=[year_validator],
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        blank=True,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        'Title', verbose_name='Произведение', on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        'Genre', verbose_name='Жанр', on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Category(models.Model):
    """Модель для создания категорий к произведениям."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:30]


class Genre(models.Model):
    """Модель для создания жанров к произведениям."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:30]


class Review(models.Model):
    """Модель для создания отзывов."""

    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveIntegerField(
        verbose_name='оценка',
        validators=[
            MinValueValidator(1, message='Введите оценку от 1 до 10'),
            MaxValueValidator(10, message='Введите оценку от 1 до 10'),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            UniqueConstraint(fields=['author', 'title'], name='unique_review'),
        )

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    """Модель для создания комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментарий',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]
