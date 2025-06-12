from django.urls import path, include
from .views import StatusViewSet
from .social.urls import urlpatterns as social_urlpatterns

urlpatterns = [
    path('', StatusViewSet.as_view({'get': 'status'})),
    path(r'^social/', include(social_urlpatterns)),
]
