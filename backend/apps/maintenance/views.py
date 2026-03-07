from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import MaintenanceCategory, MaintenanceRecord, MaintenanceReminder
from .serializers import (
    MaintenanceCategorySerializer,
    MaintenanceRecordSerializer,
    MaintenanceReminderSerializer,
)


class MaintenanceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaintenanceCategory.objects.all()
    serializer_class = MaintenanceCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["part_name", "brand", "notes"]
    ordering_fields = ["service_date", "odometer_km", "cost"]

    def get_queryset(self):
        qs = MaintenanceRecord.objects.filter(vehicle__owner=self.request.user)
        vehicle_id = self.request.query_params.get("vehicle")
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        return qs


class MaintenanceReminderViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceReminderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["due_date", "due_odometer_km"]

    def get_queryset(self):
        qs = MaintenanceReminder.objects.filter(vehicle__owner=self.request.user)
        vehicle_id = self.request.query_params.get("vehicle")
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs
