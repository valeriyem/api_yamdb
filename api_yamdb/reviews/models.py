from django.db import models

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
