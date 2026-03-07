from django.contrib import admin
from .models import OdometerLog, Trip, FuelRefill


@admin.register(OdometerLog)
class OdometerLogAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "odometer_km", "recorded_at"]
    raw_id_fields = ["vehicle"]


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "start_at", "end_at", "distance_km"]
    raw_id_fields = ["vehicle"]


@admin.register(FuelRefill)
class FuelRefillAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "refill_date", "liters", "total_cost", "fuel_efficiency_km_per_liter"]
    list_filter = ["is_full_tank"]
    raw_id_fields = ["vehicle"]
