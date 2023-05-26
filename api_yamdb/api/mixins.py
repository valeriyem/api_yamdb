"""Миксины для API вьюсетов."""
from rest_framework import mixins, viewsets


class DestroyCreateListMixins(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass
