from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HealthCheckViewSet

router = DefaultRouter()
router.register(r"status", HealthCheckViewSet, basename="healthcheck")


urlpatterns = [
    path("ping", HealthCheckViewSet.as_view({"get": "get_status"})),
] + router.urls