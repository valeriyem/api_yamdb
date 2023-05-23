from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet


app_name = 'api'


router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
]