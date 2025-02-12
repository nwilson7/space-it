from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from bookings.models import Booking
from launches.models import Launch


# Create your views here.
def view_your_bookings(request):
    user_id = request.user.id
    today = timezone.now().date()

    pending_bookings = Booking.objects.filter(
        cancelled=False,
        launch__launch_date__gt=today,
        cargo__launched=False,
        cargo__owner_id=user_id
    ).order_by('launch__launch_date')  # Order by launch date of associated launch

    # Find bookings where the user (owner_id=1) has launched but non-cancelled bookings
    launched_bookings = Booking.objects.filter(
        cancelled=False,
        launch__launch_date__lte=today,
        cargo__launched=True,
        cargo__owner_id=user_id
    ).order_by('launch__launch_date')  # Order by launch date of associated launch

    return render(
        request,
        "bookings/view_bookings.html",
        {
            "pending_bookings": pending_bookings,
            "launched_bookings": launched_bookings
        }
    )

def cancel_booking(request, id):
    try:
        booking = Booking.objects.get(id=id)

        # Check if already cancelled or launched
        if booking.cancelled:
            return JsonResponse({"error": "This booking has already been cancelled."})

        if booking.cargo.launched:
            return JsonResponse({"error": "The cargo for this booking has already been launched."})

        with transaction.atomic():
            Booking.objects.filter(id=id).update(cancelled=True)

            # Update remaining capacity
            new_remaining_capacity = booking.launch.remaining_capacity_kg + booking.cargo.total_weight()
            Launch.objects.filter(id=booking.launch.id).update(remaining_capacity_kg=new_remaining_capacity)

        return JsonResponse({"message": "Booking has been successfully cancelled."})

    except Booking.DoesNotExist:
        return JsonResponse({"error": "Booking not found."})