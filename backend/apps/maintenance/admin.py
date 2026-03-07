from django.contrib import admin
from .models import MaintenanceCategory, MaintenanceRecord, MaintenanceReminder


@admin.register(MaintenanceCategory)
class MaintenanceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "is_system"]


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "part_name", "brand", "cost", "service_date", "odometer_km"]
    list_filter = ["category", "service_date"]
    search_fields = ["part_name", "brand", "vehicle__name"]
    raw_id_fields = ["vehicle"]


@admin.register(MaintenanceReminder)
class MaintenanceReminderAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "name", "trigger_type", "due_date", "due_odometer_km", "status"]
    list_filter = ["trigger_type", "status"]
    search_fields = ["name", "vehicle__name"]
    raw_id_fields = ["vehicle"]
