from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["name", "make", "model", "year", "vehicle_type", "owner", "current_odometer_km", "is_active"]
    list_filter = ["vehicle_type", "fuel_type", "is_active"]
    search_fields = ["name", "make", "model", "license_plate", "owner__email"]
    raw_id_fields = ["owner"]
