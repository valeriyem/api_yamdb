from django.contrib import admin

from .models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Genre."""
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name', ]
    empty_value_display = '-пусто-'
