from django.db import models
from .validators import year_validator

class Review(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор')
    value = models.IntegerField(verbose_name='оценка')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='произведение',
                              null=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text



class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='комментарий')
    text = models.TextField()
    created = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


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
