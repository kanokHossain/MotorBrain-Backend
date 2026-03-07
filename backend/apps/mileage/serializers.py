from rest_framework import serializers
from .models import OdometerLog, Trip, FuelRefill


class OdometerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdometerLog
        fields = ["id", "vehicle", "odometer_km", "recorded_at", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]


class TripSerializer(serializers.ModelSerializer):
    distance_km = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Trip
        fields = [
            "id", "vehicle", "start_odometer_km", "end_odometer_km",
            "start_at", "end_at", "purpose", "notes", "distance_km", "created_at",
        ]
        read_only_fields = ["id", "distance_km", "created_at"]


class FuelRefillSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelRefill
        fields = [
            "id", "vehicle", "refill_date", "odometer_km", "liters",
            "cost_per_liter", "total_cost", "is_full_tank", "fuel_station", "notes",
            "fuel_efficiency_km_per_liter", "cost_per_km", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "fuel_efficiency_km_per_liter", "cost_per_km", "created_at", "updated_at"
        ]
