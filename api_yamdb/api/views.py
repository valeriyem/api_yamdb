from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Title
from .filters import TitleFilter
from .serializers import TitleSerializer


class TitleViewSet(ModelViewSet):
    """Вьюсет для обработки произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TitleFilter
