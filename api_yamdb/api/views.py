from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    """Вьюсет для обработки категорий для произведений."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete', ]
