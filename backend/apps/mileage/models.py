"""
Mileage and fuel tracking models for MotorBrain.

Tracks trips, fuel refills, and calculates fuel efficiency.
"""

from django.db import models


class OdometerLog(models.Model):
    """
    A single odometer reading entry — used to track total distance over time.
    """

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="odometer_logs",
    )
    odometer_km = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Odometer Log"
        verbose_name_plural = "Odometer Logs"
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.vehicle} — {self.odometer_km} km at {self.recorded_at:%Y-%m-%d}"


class Trip(models.Model):
    """
    A recorded trip with start/end odometer readings.
    """

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="trips",
    )
    start_odometer_km = models.DecimalField(max_digits=10, decimal_places=2)
    end_odometer_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    purpose = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"
        ordering = ["-start_at"]

    def __str__(self):
        return f"{self.vehicle} — trip on {self.start_at:%Y-%m-%d}"

    @property
    def distance_km(self):
        if self.end_odometer_km is not None:
            return self.end_odometer_km - self.start_odometer_km
        return None


class FuelRefill(models.Model):
    """
    A fuel refill record.
    Tracks liters added, cost, and odometer reading to calculate efficiency.
    """

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="fuel_refills",
    )
    refill_date = models.DateField()
    odometer_km = models.DecimalField(max_digits=10, decimal_places=2)
    liters = models.DecimalField(max_digits=8, decimal_places=3)
    cost_per_liter = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_full_tank = models.BooleanField(default=True)
    fuel_station = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Calculated after entry — km/L since last full tank fill
    fuel_efficiency_km_per_liter = models.DecimalField(
        max_digits=8, decimal_places=3, null=True, blank=True
    )
    cost_per_km = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)

    class Meta:
        verbose_name = "Fuel Refill"
        verbose_name_plural = "Fuel Refills"
        ordering = ["-refill_date", "-odometer_km"]

    def __str__(self):
        return f"{self.vehicle} — {self.liters}L on {self.refill_date}"
