from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from .models import Launch, Booking, Transaction
from cargo.models import Cargo
from celery import shared_task

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
                continue  # Skip invalid bookings

            try:
                with transaction.atomic():
                    # Atomically check and mark cargo as launched
                    updated = Cargo.objects.filter(
                        id=cargo.id,
                        launched=False
                    ).update(launched=True)

                    if not updated:
                        print(f"Cargo {cargo.id} already processed. Skipping.")
                        continue  # Skip if already launched

                    # Generate transaction note
                    note = (
                        f"Cargo: {cargo.cargoname} x {cargo.number_of_items} "
                        f"(Total weight = {cargo.total_weight()}) | "
                        f"Launch date: {launch.launch_date} | "
                        f"Rocket: {launch.rocket.name} | "
                        f"Destination: {launch.destination.name}"
                    )

                    # Create transaction
                    Transaction.objects.create(
                        sender=cargo.owner,
                        recipient=launch.rocket.owner,
                        amount=booking.payment_amount,
                        note=note
                    )

            except Exception as e:
                print(f"Error processing booking {booking.id}: {str(e)}")