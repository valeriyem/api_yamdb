from django.contrib import admin

from .models import Title, Category, Genre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Title."""
    list_display = [
        'name',
        'year',
        'description',
        'category',
    ]
    search_fields = ['name', ]
    list_filter = ['category', ]
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Category."""
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name', ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Genre."""
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name', ]
    empty_value_display = '-пусто-'