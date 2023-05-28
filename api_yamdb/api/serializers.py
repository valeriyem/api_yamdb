from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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

    def validate(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        try:
            user, _ = User.objects.get_or_create(
                username=username,
                email=email,
            )
        except IntegrityError:
            raise serializers.ValidationError('Это имя или email уже занято')
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


class UserSerializer(serializers.ModelSerializer):
    """Сериалилзация данных пользователя."""

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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User

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


class UserEditSerializer(serializers.ModelSerializer):
    """Сериализация редактирования данных пользователя."""

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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация модели категорий к произведениям."""
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
        ]


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация модели жанров к произведениям."""
    lookup_field = 'slug'

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
            'rating',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов к произведениям."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id'),
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данное произведение',
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к отзывам."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field="text")

    class Meta:
        fields = '__all__'
        model = Comment
