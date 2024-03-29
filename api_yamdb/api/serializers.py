from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных пользователя."""
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_empty(self, data):
        username = data.get('username')
        email = data.get('email')
        if not username:
            raise serializers.ValidationError(
                'Имя пользователя не может быть пустым',
            )
        if not email:
            raise serializers.ValidationError('Email не может быть пустым')
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация запросов на регистрацию."""
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True,
    )
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено!')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']

        if User.objects.filter(
            username=username,
            email=email,
        ).exists():
            return validated_data

        if (
            User.objects.filter(username=username).exists()
            or User.objects.filter(email=email).exists()
        ):
            raise serializers.ValidationError('This user already exists!')
        return validated_data


class TokenSerializer(serializers.Serializer):
    """Сериализация токена."""
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=settings.LIMIT_CODE,
        required=True,
    )

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class UserSerializer(BaseUserSerializer):
    """Сериализация данных пользователя."""
    def validate(self, data):
        data = super().validate(data)
        # Добавить дополнительную валидацию, если необходимо
        return data


class UserEditSerializer(BaseUserSerializer):
    """Сериализация редактирования данных пользователя."""
    class Meta(BaseUserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация модели категорий к произведениям."""
    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
        ]
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация модели жанров к произведениям."""
    class Meta:
        model = Genre
        fields = [
            'name',
            'slug',
        ]
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация модели произведений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализация модели произведений с правами только для чтения."""
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True,
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов к произведениям."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данное произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field="text")

    class Meta:
        fields = '__all__'
        model = Comment
