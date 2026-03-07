from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            "id", "name", "make", "model", "year", "vehicle_type", "fuel_type",
            "license_plate", "vin", "color", "image", "current_odometer_km",
            "is_active", "created_at", "updated_at", "owner_email",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "owner_email"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
