from django.db import models
from rockets.models import Rocket
from destination.models import Destination
from decimal import Decimal

class Launch(models.Model):
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    launch_date = models.DateField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    remaining_capacity_kg = models.FloatField()
    launch_cost = models.FloatField()
    price_per_kg = models.FloatField()

    def save(self, *args, **kwargs):
        required_fuel = Decimal(self.destination.distance) * Decimal(2) * Decimal(self.rocket.fuel_consumption_rate)

        if required_fuel > Decimal(self.rocket.fuel_capacity):
            raise ValueError("Rocket does not have enough fuel to reach the destination and return.")

        if Launch.objects.filter(rocket=self.rocket, launch_date=self.launch_date).exists():
            raise ValueError("This rocket is already scheduled for a launch on this date.")

        self.remaining_capacity_kg = Decimal(self.rocket.cargo_capacity_kg)
        self.launch_cost = Decimal(self.destination.distance) * (Decimal(self.rocket.fuel_consumption_rate) * Decimal(self.rocket.fuel_cost))

        super().save(*args, **kwargs)