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
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.note:
            self.note = (
                f"Cargo: {self.sender.cargo_set.first().cargoname} x {self.sender.cargo_set.first().number_of_items} "
                f"(Total weight = {self.sender.cargo_set.first().total_weight()}) | "
                f"Launch date: {self.sender.booking_set.first().launch.launch_date} | "
                f"Rocket: {self.sender.booking_set.first().launch.rocket.name} | "
                f"Destination: {self.sender.booking_set.first().launch.destination.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} → {self.recipient}: £{self.amount}"