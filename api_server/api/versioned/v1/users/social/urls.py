from django.urls import path, include
from .views import AuthViewSet, UserJoinViewSet

# create_google
urlpatterns = [
    path('google', AuthViewSet.as_view({'post': 'create_google'})),
    path('join', UserJoinViewSet.as_view({'post': 'create'})),
]
