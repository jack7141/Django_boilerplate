from django.urls import path, include
from .views import StatusViewSet

urlpatterns = [
    path('google', StatusViewSet.as_view({'get': 'status'})),
]
