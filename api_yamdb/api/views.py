from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from reviews.models import Title, Category
from .filters import TitleFilter
from .serializers import TitleSerializer, CategorySerializer


class TitleViewSet(ModelViewSet):
    """Вьюсет для обработки произведений."""
    queryset = Title.objects.all()
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
