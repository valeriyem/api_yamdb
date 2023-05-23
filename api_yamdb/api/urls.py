from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet


app_name = 'api'


router = DefaultRouter()

router.register(r'genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router.urls)),
]
