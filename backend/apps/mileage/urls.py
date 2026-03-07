from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OdometerLogViewSet, TripViewSet, FuelRefillViewSet

router = DefaultRouter()
router.register(r"odometer", OdometerLogViewSet, basename="odometer-log")
router.register(r"trips", TripViewSet, basename="trip")
router.register(r"fuel", FuelRefillViewSet, basename="fuel-refill")

urlpatterns = [
    path("", include(router.urls)),
]
