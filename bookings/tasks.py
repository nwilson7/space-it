from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from .models import Launch, Booking, Transaction
from cargo.models import Cargo
from celery import shared_task

# In tasks.py
@shared_task
def daily_task():
    today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
    launches_today = Launch.objects.filter(
        launch_date__gte=today_start,
        launch_date__lt=today_start + timedelta(days=1)
    )

    for launch in launches_today:
        bookings = Booking.objects.filter(launch=launch, cancelled=False)

        for booking in bookings:
            cargo = booking.cargo
            if not cargo:
                continue

            try:
                with transaction.atomic():
                    # Atomically check and mark cargo as launched
                    updated = Cargo.objects.filter(
                        id=cargo.id,
                        launched=False
                    ).update(launched=True)

                    if not updated:
                        continue

                    # Generate transaction note
                    note = (
                        f"Cargo: {cargo.cargoname} x {cargo.number_of_items} "
                        f"(Total weight = {cargo.total_weight()}) | "
                        f"Launch date: {launch.launch_date} | "
                        f"Rocket: {launch.rocket.name} | "
                        f"Destination: {launch.destination.name}"
                    )

                    # Explicitly link to the current booking
                    Transaction.objects.create(
                        sender=cargo.owner,
                        recipient=launch.rocket.owner,
                        amount=booking.payment_amount,
                        note=note,
                        booking=booking  # <-- Add this line
                    )

            except Exception as e:
                print(f"Error processing booking {booking.id}: {str(e)}")