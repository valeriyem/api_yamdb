from rest_framework import serializers

from reviews.models import Title


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
