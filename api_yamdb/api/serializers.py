from rest_framework import serializers
from reviews.models import Comment, Review, Title

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
