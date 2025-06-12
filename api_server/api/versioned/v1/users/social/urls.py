from django.urls import path, include
from .views import AuthViewSet, UserJoinViewSet

# create_google
urlpatterns = [
    path('google', AuthViewSet.as_view({'post': 'create_google'})),
    path('kakao', AuthViewSet.as_view({'post': 'create_kakao'})),
    path('join', UserJoinViewSet.as_view({'post': 'create'})),
]
