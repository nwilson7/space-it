from django.db import models
from rockets.models import Rocket
from destination.models import Destination
from decimal import Decimal
# Create your models here.
class Launch(models.Model):
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    launch_date = models.DateField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    remaining_capacity_kg = models.FloatField()
    launch_cost = models.FloatField()
    price_per_kg = models.FloatField()

    def save(self, *args, **kwargs):
        print("starting launch.save")
        required_fuel = Decimal(self.destination.distance) * Decimal(2) * Decimal(self.rocket.fuel_consumption_rate)
        print("required fuel calculations completed")
        if required_fuel > Decimal(self.rocket.fuel_capacity):
            raise ValueError("Rocket does not have enough fuel to reach the destination and return.")
        print("Rocket has sufficient fuel")
        if Launch.objects.filter(rocket=self.rocket, launch_date=self.launch_date).exists():
            print("This rocket is already scheduled for a launch on this date.")
            raise ValueError("This rocket is already scheduled for a launch on this date.")
        print("Rocket is available")
        self.remaining_capacity_kg = Decimal(self.rocket.cargo_capacity_kg)
        self.launch_cost = Decimal(self.destination.distance) * (Decimal(self.rocket.fuel_consumption_rate) * Decimal(self.rocket.fuel_cost))
        print("updating the remaining_capacity_kg")
        super().save(*args, **kwargs)