from django.db import models
from users.models import User
from destination.models import Destination
# Create your models here.
class Cargo(models.Model):
    cargoname = models.CharField(max_length=255)
    weight_per_item = models.FloatField(help_text="kg")
    number_of_items = models.PositiveIntegerField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'cargo_owner'})
    launched = models.BooleanField(default=False)

    def total_weight(self):
        return round(self.weight_per_item * self.number_of_items,3)

    def is_booked(self):
        return self.booking_set.filter(cancelled=False).exists()