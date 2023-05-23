from rest_framework import serializers

from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация модели категорий к произведениям."""

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
        ]
