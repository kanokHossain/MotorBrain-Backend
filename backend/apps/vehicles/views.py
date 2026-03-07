from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "make", "model", "license_plate"]
    ordering_fields = ["created_at", "year", "name"]

    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user, is_active=True)
