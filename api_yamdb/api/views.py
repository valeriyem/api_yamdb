from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Title
from .serializers import TitleSerializer


class TitleViewSet(ModelViewSet):
    """Вьюсет для обработки произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
