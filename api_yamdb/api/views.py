from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters, permissions, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import permission_classes

from api.serializers import (RegistrationSerializer, TokenSerializer,
                             UserEditSerializer, UserSerializer)
from reviews.models import Title
from users.models import User

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly, IsStaffOrAuthorOrReadOnly,
                          IsAdminOrSuperUser, IsAuthenticatedOrReadOnly
                          )

from .serializers import TitleSerializer
from reviews.models import Title, Category, Genre Comment, Review
from .filters import TitleFilter

from .permissions import IsAuthorIsModeratorIsAdminIsSuperUser
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer)



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Регистрация пользователя"""
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
    """Получение jwt токена"""
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


class UserViewSet(viewsets.ModelViewSet):
    """Администратор получает список пользователей или создает нового"""

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
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all()
    queryset = Title.objects.annotate(
      rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = TitleFilter


class CategoryViewSet(ModelViewSet):
    """Вьюсет для обработки категорий для произведений."""
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete', ]


class GenreViewSet(ModelViewSet):
    """Вьюсет для обработки жанров для произведений."""
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete', ]
    

class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Review"""
    permission_classes = (IsStaffOrAuthorOrReadOnly,)
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorIsModeratorIsAdminIsSuperUser)

    def get_queryset(self):
        title_id =self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        new_queryset = title.reviews.all()
        return new_queryset


    def perform_create(self,serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Comment."""
    permission_classes = (IsStaffOrAuthorOrReadOnly,)
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorIsModeratorIsAdminIsSuperUser)

    def get_queryset(self):
        review_id =self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self,serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)
