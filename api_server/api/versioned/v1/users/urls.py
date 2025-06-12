from django.urls import path, include

from .social.views import AuthViewSet
from .views import UserViewSet
from .social.urls import urlpatterns as social_urlpatterns

urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('logout', UserViewSet.as_view({'post': 'logout'})),
    path('social/', include(social_urlpatterns)),
]
