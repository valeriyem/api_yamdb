from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets

from reviews.models import Comment, Review, Title

from .permissions import IsAuthorIsModeratorIsAdminIsSuperUser
from .serializers import (ReviewSerializer, CommentSerializer)


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



