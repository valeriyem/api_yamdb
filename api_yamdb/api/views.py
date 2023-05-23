from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Genre
from .serializers import GenreSerializer


class GenreViewSet(ModelViewSet):
    """Вьюсет для обработки жанров для произведений."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete', ]
