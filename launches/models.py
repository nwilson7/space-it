from django.db import models
from rockets.models import Rocket
from destination.models import Destination
# Create your models here.
class Launch(models.Model):
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    launch_date = models.DateField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    remaining_capacity_kg = models.FloatField()
    launch_cost = models.FloatField()
    price_per_kg = models.FloatField()

    def save(self, *args, **kwargs):
        required_fuel = self.destination.distance * 2 * self.rocket.fuel_consumption_rate
        if required_fuel > self.rocket.fuel_capacity:
            raise ValueError("Rocket does not have enough fuel to reach the destination and return.")

        if Launch.objects.filter(rocket=self.rocket, launch_date=self.launch_date).exists():
            raise ValueError("This rocket is already scheduled for a launch on this date.")

        self.remaining_capacity_kg = self.rocket.cargo_capacity_kg

        self.launch_cost = self.destination.distance * (self.rocket.fuel_consumption_rate * self.rocket.fuel_cost)

        super().save(*args, **kwargs)