from rest_framework import serializers
from .models import AIInsight, VehicleHealthScore


class AIInsightSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source="vehicle.name", read_only=True)

    class Meta:
        model = AIInsight
        fields = [
            "id", "vehicle", "vehicle_name", "insight_type", "priority",
            "title", "summary", "detail", "confidence_score",
            "is_dismissed", "generated_at", "valid_until",
        ]
        read_only_fields = ["id", "generated_at", "vehicle_name"]


class VehicleHealthScoreSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source="vehicle.name", read_only=True)

    class Meta:
        model = VehicleHealthScore
        fields = [
            "id", "vehicle", "vehicle_name", "score",
            "maintenance_score", "mileage_score", "fuel_score", "computed_at",
        ]
        read_only_fields = fields
