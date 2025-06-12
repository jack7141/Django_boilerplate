from django.urls import path, include
from .views import UserViewSet
from .social.urls import urlpatterns as social_urlpatterns

urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('social/', include(social_urlpatterns)),
]
