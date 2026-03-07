from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from .models import OdometerLog, Trip, FuelRefill
from .serializers import OdometerLogSerializer, TripSerializer, FuelRefillSerializer


class OdometerLogViewSet(viewsets.ModelViewSet):
    serializer_class = OdometerLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["recorded_at", "odometer_km"]

    def get_queryset(self):
        qs = OdometerLog.objects.filter(vehicle__owner=self.request.user)
        vehicle_id = self.request.query_params.get("vehicle")
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        return qs


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["start_at", "distance_km"]

    def get_queryset(self):
        qs = Trip.objects.filter(vehicle__owner=self.request.user)
        vehicle_id = self.request.query_params.get("vehicle")
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        return qs


class FuelRefillViewSet(viewsets.ModelViewSet):
    serializer_class = FuelRefillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["refill_date", "odometer_km", "liters"]

    def get_queryset(self):
        qs = FuelRefill.objects.filter(vehicle__owner=self.request.user)
        vehicle_id = self.request.query_params.get("vehicle")
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        return qs
