"""
Vehicle models for MotorBrain.

Represents cars and bikes owned by users.
"""

from django.db import models
from django.conf import settings


class Vehicle(models.Model):
    """
    A vehicle (car or bike) owned by a user.
    """

    class VehicleType(models.TextChoices):
        CAR = "car", "Car"
        BIKE = "bike", "Bike"
        TRUCK = "truck", "Truck"
        OTHER = "other", "Other"

    class FuelType(models.TextChoices):
        PETROL = "petrol", "Petrol"
        DIESEL = "diesel", "Diesel"
        ELECTRIC = "electric", "Electric"
        HYBRID = "hybrid", "Hybrid"
        CNG = "cng", "CNG"
        LPG = "lpg", "LPG"
        OCTANE = "octane", "Octane"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehicles",
    )

    name = models.CharField(max_length=100, help_text="User-defined name, e.g. 'My Honda'")
    make = models.CharField(max_length=100, help_text="Manufacturer, e.g. 'Honda'")
    model = models.CharField(max_length=100, help_text="Model name, e.g. 'Civic'")
    year = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices, default=VehicleType.CAR)
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices, default=FuelType.PETROL)

    license_plate = models.CharField(max_length=20, blank=True)
    vin = models.CharField(max_length=17, blank=True, verbose_name="VIN")
    color = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to="vehicles/", null=True, blank=True)

    # Current odometer reading — updated with each mileage/maintenance log
    current_odometer_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.owner.email})"
