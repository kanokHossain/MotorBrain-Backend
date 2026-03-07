"""
Celery tasks for mileage-based reminder triggers.
"""

from celery import shared_task


@shared_task
def recalculate_fuel_efficiency(fuel_refill_id: int):
    """
    After a new fuel refill is logged, compute fuel efficiency
    based on distance since last full-tank fill.
    """
    from .models import FuelRefill

    try:
        refill = FuelRefill.objects.get(id=fuel_refill_id)
    except FuelRefill.DoesNotExist:
        return "Refill not found."

    if not refill.is_full_tank:
        return "Not a full tank fill — skipping efficiency calculation."

    prev_full_fill = (
        FuelRefill.objects.filter(
            vehicle=refill.vehicle,
            is_full_tank=True,
            odometer_km__lt=refill.odometer_km,
        )
        .order_by("-odometer_km")
        .first()
    )

    if not prev_full_fill:
        return "No previous full fill — cannot calculate efficiency."

    distance = float(refill.odometer_km) - float(prev_full_fill.odometer_km)
    liters = float(refill.liters)

    if liters > 0 and distance > 0:
        km_per_liter = distance / liters
        refill.fuel_efficiency_km_per_liter = round(km_per_liter, 3)

        if refill.total_cost and distance > 0:
            refill.cost_per_km = round(float(refill.total_cost) / distance, 3)

        refill.save(update_fields=["fuel_efficiency_km_per_liter", "cost_per_km"])
        return f"Efficiency: {km_per_liter:.2f} km/L"

    return "Invalid data — distance or liters is zero."
