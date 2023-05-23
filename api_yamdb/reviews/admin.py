from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Category."""
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name', ]
    empty_value_display = '-пусто-'
