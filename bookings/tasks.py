from django.utils import timezone
from datetime import datetime, timedelta
from .models import Launch, Booking
from destination.models import Destination
from celery import shared_task

@shared_task
def daily_task():
    # Log the current time at the start of the task
    start_time = timezone.now()
    print(f"Starting daily task at {start_time}")

    # Get today's date at midnight
    today_start = timezone.make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))

    # Get the launches that are happening today
    launches_today = Launch.objects.filter(launch_date__gte=today_start,
                                           launch_date__lt=today_start + timedelta(days=1))

    print(f"Today's launches at {timezone.now()}:", launches_today)

    # For each launch, find associated bookings where cancelled=False
    for launch in launches_today:
        bookings = Booking.objects.filter(launch=launch, cancelled=False)

        for booking in bookings:
            cargo = booking.cargo
            if cargo and not cargo.launched:
                cargo.update(launched=True)
                print(f"Updating cargo: {cargo.cargoname} at {timezone.now()}")


    try:
        # Insert a new destination into the destination_destination table
        random_link = "https://example.com/random_image.jpg"  # Random link to an image
        new_destination = Destination.objects.create(
            name="Antarctica",  # Set the name as needed
            distance=0.5,
            link_to_image=random_link
        )
        print(f"New destination added: {new_destination.name} with distance {new_destination.distance} and image {new_destination.link_to_image}")
    except Exception as e:
        print(f"Error creating destination: {str(e)}")

    # Log the end time of the task
    end_time = timezone.now()
    print(f"Task completed at {end_time}")

    return 'Task Completed'
