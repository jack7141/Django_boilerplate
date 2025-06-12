from django.urls import path, include
from .views import StatusViewSet, AuthViewSet

# create_google
urlpatterns = [
    path('', StatusViewSet.as_view({'get': 'status'})),
    path('google', AuthViewSet.as_view({'post': 'create_google'})),
]
