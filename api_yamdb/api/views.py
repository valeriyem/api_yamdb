from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (ReadOnlyTitleSerializer, RegistrationSerializer,
                             TokenSerializer, UserEditSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title
# Импорты для работы с Юзером
from users.models import User

# Импорты для работы с произведениями
from .filters import TitleFilter
from .mixins import DestroyCreateListMixins
from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperUser,
                          IsAuthenticatedOrReadOnly, IsStaffOrAuthorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Регистрация пользователя."""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    email = serializer.data['email']
    user, _ = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на сайте YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Получение jwt токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username'],
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code'],
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """Администратор получает список пользователей или создает нового."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = (IsAdminOrSuperUser, IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me_info(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserEditSerializer(
                user, data=request.data, partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(ModelViewSet):
    """Вьюсет для обработки произведений."""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CategoryViewSet(DestroyCreateListMixins):
    """Вьюсет для обработки категорий для произведений."""
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class GenreViewSet(DestroyCreateListMixins):
    """Вьюсет для обработки жанров для произведений."""
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class ReviewViewSet(ModelViewSet):
    """Вьюсет для объектов модели Review"""
    permission_classes = (IsStaffOrAuthorOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(ModelViewSet):
    """Вьюсет для объектов модели Comment."""
    permission_classes = (IsStaffOrAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)
