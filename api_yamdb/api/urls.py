from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

app_name ='api'
router = DefaultRouter()
router.register(r'title/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]