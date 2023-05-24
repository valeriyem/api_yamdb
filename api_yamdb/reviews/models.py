from django.db import models

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
        db_index=True,
        blank=True,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:30]


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