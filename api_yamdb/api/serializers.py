from rest_framework import serializers
from reviews.models import (Title, Category, Genre, 
                            Comment, Review)


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация модели произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(required=False)
      
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
        

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context["request"].method !="POST":
            return data
        title = get_object_or_404(Title,
                                  pk=self.context["view"].kwargs.get("title_id"))
        author = self.context["request"].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на данное произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field="text")

    class Meta:
        fields = '__all__'
        model = Comment
