from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .social.views import AuthViewSet
from .views import UserViewSet
from .social.urls import urlpatterns as social_urlpatterns


router = DefaultRouter()
router.register("", UserViewSet)

# OAuth 인증 완료 되면, 토큰 발급 -> User Create
urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('refresh-token', UserViewSet.as_view({'post': 'refresh_token'})),
    path('logout', UserViewSet.as_view({'post': 'logout'})),
    path('social/', include(social_urlpatterns)),
] + router.urls
