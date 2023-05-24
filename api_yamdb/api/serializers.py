from rest_framework import serializers

from reviews.models import Title, Category, Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация модели произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация модели категорий к произведениям."""

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
        ]


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация модели жанров к произведениям."""

    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
            'slug',
        ]