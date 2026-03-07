from rest_framework import serializers
from .models import MaintenanceCategory, MaintenanceRecord, MaintenanceReminder


class MaintenanceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceCategory
        fields = ["id", "name", "icon", "is_system"]
        read_only_fields = ["id"]


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    vehicle_name = serializers.CharField(source="vehicle.name", read_only=True)

    class Meta:
        model = MaintenanceRecord
        fields = [
            "id", "vehicle", "vehicle_name", "category", "category_name",
            "part_name", "brand", "cost", "service_date", "odometer_km",
            "notes", "receipt_image", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "vehicle_name", "category_name"]


class MaintenanceReminderSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source="vehicle.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = MaintenanceReminder
        fields = [
            "id", "vehicle", "vehicle_name", "category", "category_name", "last_record",
            "name", "trigger_type", "interval_days", "due_date",
            "interval_km", "due_odometer_km", "status", "notification_sent",
            "snoozed_until", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "vehicle_name", "category_name", "notification_sent"]
