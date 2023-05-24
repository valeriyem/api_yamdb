from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import registration, get_jwt_token

from .views import CommentViewSet, ReviewViewSet, TitleViewSet

app_name ='api'
router = DefaultRouter()
router.register(r'title/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+/comments',
                CommentViewSet, basename='comments')

router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
