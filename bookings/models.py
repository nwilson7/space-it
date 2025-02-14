from django.db import models, transaction
from cargo.models import Cargo
from users.models import User
from launches.models import Launch

# Create your models here.
class Booking(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    payment_amount = models.FloatField()
    cancelled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        with transaction.atomic():
            if self.cargo.destination != self.launch.destination:
                raise ValueError("Cargo destination and launch destination must be the same.")

            if not self.payment_amount:
                self.payment_amount = self.cargo.total_weight() * self.launch.price_per_kg

            self.payment_amount = round(self.payment_amount, 2)

            if self.launch.remaining_capacity_kg - self.cargo.total_weight() < 0:
                raise ValueError("Not enough remaining capacity on the rocket for this cargo.")

            self.launch.remaining_capacity_kg -= self.cargo.total_weight()
            Launch.objects.filter(id=self.launch.id).update(remaining_capacity_kg=self.launch.remaining_capacity_kg)

            super().save(*args, **kwargs)

class Transaction(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    amount = models.FloatField()
    note = models.TextField(blank=True, null=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)  # Store Booking ID
    timestamp = models.DateTimeField(auto_now_add=True)

    # In models.py (Transaction model)
    def save(self, *args, **kwargs):
        # Only auto-generate note if not provided
        if not self.note:
            if self.booking:  # Use the linked booking if available
                cargo = self.booking.cargo
                self.note = (
                    f"Cargo: {cargo.cargoname} x {cargo.number_of_items} "
                    f"(Total weight = {cargo.total_weight()}) | "
                    f"Launch date: {self.booking.launch.launch_date} | "
                    f"Rocket: {self.booking.launch.rocket.name} | "
                    f"Destination: {self.booking.launch.destination.name}"
                )
            else:
                self.note = "No associated cargo or booking found."
        super().save(*args, **kwargs)