"""Миксины для API вьюсетов."""
from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrSuperUser


class DestroyCreateListMixins(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Для вьюсетов моделей Category и Genre."""

    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)
    # lookup_field = 'slug'
