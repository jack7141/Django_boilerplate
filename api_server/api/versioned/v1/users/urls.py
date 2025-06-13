from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .social.views import AuthViewSet
from .views import UserViewSet
from .social.urls import urlpatterns as social_urlpatterns


router = DefaultRouter()
router.register("", UserViewSet)


urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('refresh-token', UserViewSet.as_view({'post': 'refresh_token'})),
    path('logout', UserViewSet.as_view({'post': 'logout'})),
    path('social/', include(social_urlpatterns)),
] + router.urls
