from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from bookings.models import Booking, Transaction
from launches.models import Launch
from users.decorators import role_required, login_required

@role_required('cargo_owner')
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

@role_required('cargo_owner')
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
    
@login_required
def view_transaction(request, id):
    # Get the transaction based on booking_id
    transaction = get_object_or_404(Transaction, booking_id=id)
    
    if request.user.id not in [transaction.sender.id,transaction.recipient.id]:
        return HttpResponseForbidden("You are not authorized to view this transaction.")
    
    # Render the transaction details
    return render(request, 'bookings/view_transaction.html', {'transaction': transaction})

@login_required
def view_your_transactions(request):
    if request.user.role == "cargo_owner":
        transactions = Transaction.objects.filter(sender__id=request.user.id)
    else:
        transactions = Transaction.objects.filter(recipient__id=request.user.id)

    # Render the transactions in the template
    return render(request, 'bookings/view_your_transactions.html', {'transactions': transactions,'role': request.user.role})