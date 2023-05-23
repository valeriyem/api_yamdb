from rest_framework import serializers

from reviews.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация модели жанров к произведениям."""

    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
            'slug',
        ]
