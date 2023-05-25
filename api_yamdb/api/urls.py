from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import get_jwt_token, registration

from .views import TitleViewSet

app_name = 'api'


router = DefaultRouter()

router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
