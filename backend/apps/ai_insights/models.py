"""
AI Insights models for MotorBrain.

Stores predictive maintenance insights and AI-generated recommendations.
"""

from django.db import models
from django.conf import settings


class AIInsight(models.Model):
    """
    An AI-generated insight or prediction for a vehicle.
    """

    class InsightType(models.TextChoices):
        MAINTENANCE_PREDICTION = "maintenance_prediction", "Maintenance Prediction"
        FUEL_EFFICIENCY = "fuel_efficiency", "Fuel Efficiency"
        COST_ANALYSIS = "cost_analysis", "Cost Analysis"
        HEALTH_SCORE = "health_score", "Vehicle Health Score"
        RECOMMENDATION = "recommendation", "General Recommendation"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="ai_insights",
    )
    insight_type = models.CharField(max_length=50, choices=InsightType.choices)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    detail = models.TextField(blank=True, help_text="Detailed explanation and reasoning")
    confidence_score = models.FloatField(
        null=True, blank=True, help_text="AI confidence 0.0 to 1.0"
    )
    data_snapshot = models.JSONField(
        default=dict, blank=True, help_text="Input data used to generate insight"
    )
    is_dismissed = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "AI Insight"
        verbose_name_plural = "AI Insights"
        ordering = ["-generated_at"]

    def __str__(self):
        return f"{self.vehicle} — {self.title}"


class VehicleHealthScore(models.Model):
    """
    Periodic vehicle health score snapshots computed by AI.
    """

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="health_scores",
    )
    score = models.FloatField(help_text="Overall health score 0 to 100")
    maintenance_score = models.FloatField(null=True, blank=True)
    mileage_score = models.FloatField(null=True, blank=True)
    fuel_score = models.FloatField(null=True, blank=True)
    computed_at = models.DateTimeField(auto_now_add=True)
    snapshot = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Vehicle Health Score"
        ordering = ["-computed_at"]

    def __str__(self):
        return f"{self.vehicle} — Score: {self.score:.1f}"
