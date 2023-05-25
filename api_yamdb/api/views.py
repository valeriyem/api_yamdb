from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, permissions, viewsets
from rest_framework.viewsets import ModelViewSet

from reviews.models import Title, Category, Genre Comment, Review
from .filters import TitleFilter

from .permissions import IsAuthorIsModeratorIsAdminIsSuperUser
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer)


class TitleViewSet(ModelViewSet):
    """Вьюсет для обработки произведений."""
    #queryset = Title.objects.all()
    queryset = Title.objects.annotate(
      rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TitleFilter


class CategoryViewSet(ModelViewSet):
    """Вьюсет для обработки категорий для произведений."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete', ]


class GenreViewSet(ModelViewSet):
    """Вьюсет для обработки жанров для произведений."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete', ]
    

class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Review"""
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
