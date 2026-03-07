from django.contrib import admin
from .models import AIInsight, VehicleHealthScore


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "insight_type", "priority", "title", "confidence_score", "is_dismissed", "generated_at"]
    list_filter = ["insight_type", "priority", "is_dismissed"]
    search_fields = ["title", "vehicle__name"]


@admin.register(VehicleHealthScore)
class VehicleHealthScoreAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "score", "computed_at"]
    raw_id_fields = ["vehicle"]
