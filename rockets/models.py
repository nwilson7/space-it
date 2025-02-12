from django.db import models
from users.models import User
from decimal import Decimal
# Create your models here.
class Rocket(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'rocket_owner'})
    cargo_capacity_kg = models.FloatField(help_text="kgs")
    fuel_consumption_rate = models.FloatField(help_text="Tonnes per AU")
    fuel_cost = models.DecimalField(max_digits=10,decimal_places=2,help_text="£ per tonne")
    fuel_capacity = models.FloatField(help_text="tonnes")
    range_au = models.FloatField(editable=False,help_text="AUs")

    def save(self, *args, **kwargs):
        self.range_au = round(float(self.fuel_capacity) / float(self.fuel_consumption_rate),3)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - £{self.fuel_cost:.2f}"  # Format fuel_cost to 2 decimal places