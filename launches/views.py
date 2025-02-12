from django.db.models import Q, Count, Sum, F
from django.shortcuts import render, get_object_or_404, redirect
from .models import Launch, Rocket, Destination
from cargo.models import Cargo
from .forms import LaunchForm
from django.contrib import messages
from django.http import JsonResponse
import json
import decimal
from django.core.exceptions import ValidationError
from datetime import date
from bookings.models import Booking
from django.db import models, transaction


# REPLACE 2 WITH THE USER_ID IN SESSION
def view_your_launches(request):
    user_id = request.user.id
    launches = Launch.objects.filter(rocket__owner_id=user_id).order_by('launch_date')
    launches = launches.annotate(
        number_of_bookings=Count(
            'booking',
            filter=Q(booking__launch__rocket__owner_id=user_id, booking__cancelled=False),
            distinct=True
        )
    )

    for launch in launches:
        total_revenue = sum(booking.payment_amount for booking in launch.booking_set.filter(cancelled=False))
        total_profit = total_revenue - launch.launch_cost
        launch.total_profit = total_profit

    today = date.today()
    return render(request, "launches/view_launches.html", {"launches": launches, "today": today})

def view_all_launches(request):
    user_id = request.user.id
    today = date.today()
    launches = Launch.objects.filter(launch_date__gt=today).order_by('remaining_capacity_kg', 'launch_date')
    launches = launches.annotate(
        number_of_your_bookings=Count(
            'booking',
            filter=Q(booking__cargo__owner_id=user_id, booking__cancelled=False),
            distinct=True
        )
    )
    # Sort launches: first by remaining_capacity_kg, putting 0 last, and then by launch_date
    launches = sorted(launches, key=lambda launch: (launch.remaining_capacity_kg == 0, launch.launch_date))
    return render(request, "launches/view_all_launches.html", {"launches": launches})

def add_launch(request):
    # Add checks to ensure the user can only get their own rockets
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON body
            print("Data received by the server:", data)

            # Validate that required fields exist
            required_fields = ["launch_date", "destination", "rocket", "price_per_kg"]
            if not all(field in data for field in required_fields):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            # Convert and validate foreign keys
            try:
                destination = Destination.objects.get(id=int(data["destination"]))
                rocket = Rocket.objects.get(id=int(data["rocket"]))
            except (Destination.DoesNotExist, Rocket.DoesNotExist) as e:
                print("Foreign key error:", str(e))
                return JsonResponse({'status': 'error', 'message': 'Invalid foreign key reference'}, status=400)

            # Convert and round price_per_kg (Ensure Decimal type)
            try:
                price_per_kg = decimal.Decimal(str(data["price_per_kg"])).quantize(decimal.Decimal("0.01"))
            except decimal.InvalidOperation as e:
                print("Decimal conversion error:", str(e))
                return JsonResponse({'status': 'error', 'message': 'Invalid price format'}, status=400)

            # Create and save the new Launch instance
            new_launch = Launch.objects.create(
                launch_date=data["launch_date"],
                destination=destination,
                rocket=rocket,
                price_per_kg=price_per_kg
            )

            return JsonResponse({'status': 'success', 'launch_id': new_launch.id})

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        except ValueError as ve:
            print("ValueError:", str(ve))
            return JsonResponse({'status': 'error', 'message': f'Value error: {str(ve)}'}, status=400)

        except ValidationError as ve:
            print("Validation Error:", ve.message_dict)
            return JsonResponse({'status': 'error', 'message': 'Validation error', 'errors': ve.message_dict}, status=400)

        except Exception as e:
            print("Unexpected Error:", str(e))
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred', 'error': str(e)}, status=500)

    form = LaunchForm()
    return render(request, "launches/add_launch.html", {"form": form})

def edit_launch(request, id):
    # Get the Launch object to edit based on id
    launch = get_object_or_404(Launch, id=id)

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON body
            print("Data received by the server:", data)

            # Validate that required fields exist
            required_fields = ["rocket", "price_per_kg"]
            if not all(field in data for field in required_fields):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            # Convert and validate foreign keys
            try:
                rocket = Rocket.objects.get(id=int(data["rocket"]))
            except (Rocket.DoesNotExist) as e:
                print("Rocket DoesNotExist error:", str(e))
                return JsonResponse({'status': 'error', 'message': 'Invalid rocket reference'}, status=400)

            # Convert and round price_per_kg (Ensure Decimal type)
            try:
                price_per_kg = decimal.Decimal(str(data["price_per_kg"])).quantize(decimal.Decimal("0.01"))
            except decimal.InvalidOperation as e:
                print("Decimal conversion error:", str(e))
                return JsonResponse({'status': 'error', 'message': 'Invalid price format'}, status=400)

            launch.rocket = rocket
            launch.price_per_kg = price_per_kg
            launch.save()

            return JsonResponse({'status': 'success', 'launch_id': launch.id})

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        except ValueError as ve:
            print("ValueError:", str(ve))
            return JsonResponse({'status': 'error', 'message': f'Value error: {str(ve)}'}, status=400)

        except ValidationError as ve:
            print("Validation Error:", ve.message_dict)
            return JsonResponse({'status': 'error', 'message': 'Validation error', 'errors': ve.message_dict},
                                status=400)

        except Exception as e:
            print("Unexpected Error:", str(e))
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred', 'error': str(e)},
                                status=500)

    # Render the edit form with the existing launch data pre-filled
    form = LaunchForm(instance=launch)
    return render(request, "launches/edit_launch.html", {"form": form, "launch": launch})

def delete_launch(request, id):
    """Delete a launch if conditions are met"""
    launch = get_object_or_404(Launch, id=id)

    # 1. Check if the launch has already happened (i.e., launch_date is in the past)
    if launch.launch_date < date.today():
        messages.error(request, 'Launch has already happened, cannot delete.')
        return redirect('view_your_launches')

    # 2. Check if the remaining capacity is less than the rocket's cargo capacity
    if launch.remaining_capacity_kg < launch.rocket.cargo_capacity_kg:
        messages.error(request, "Remaining capacity is less than the rocket's cargo capacity, cannot delete.")
        return redirect('view_your_launches')

    # If conditions are met, delete the launch
    launch.delete()
    messages.success(request, "Launch successfully deleted!")

    return redirect("view_your_launches")

def view_booked(request, id):
    launch = get_object_or_404(Launch, id=id)
    bookings = Booking.objects.filter(launch=launch, cancelled=False)
    total_revenue = sum(booking.payment_amount for booking in bookings)
    total_profit = total_revenue - launch.launch_cost

    return render(request, "launches/view_booked.html", {
        "launch": launch,
        "bookings": bookings,
        "total_revenue": total_revenue,
        "total_profit": total_profit
    })

class CapacityExceededError(Exception):
    pass

def make_booking(request, id):
    launch = get_object_or_404(Launch, id=id)
    
    if request.method == "POST":
        try:
            # Get all cargo_ids from the post request
            selected_cargo_ids = [int(cargo_id) for cargo_id in request.POST.getlist('cargo_ids')]  # Get cargo IDs from the form
            print("selected_cargo_ids:", selected_cargo_ids)

            booked_cargo_ids = list(Booking.objects.filter(launch=launch, cancelled=False).values_list('cargo_id', flat=True))
            print("booked_cargo_ids:", booked_cargo_ids)

            cargo_ids_to_book = [cargo_id for cargo_id in selected_cargo_ids if cargo_id not in booked_cargo_ids]
            print("cargo_ids_to_book",cargo_ids_to_book)
            cargo_to_book = Cargo.objects.filter(id__in=cargo_ids_to_book)
            print("cargo_to_book",cargo_to_book)
            cargo_ids_to_cancel = [cargo_id for cargo_id in booked_cargo_ids if cargo_id not in selected_cargo_ids]
            print("cargo_ids_to_cancel",cargo_ids_to_cancel)
            bookings_to_cancel = Booking.objects.filter(cargo_id__in=cargo_ids_to_cancel, cancelled=False, launch=launch)
            print("bookings_to_cancel",bookings_to_cancel)

            for cargo in cargo_to_book:
                if cargo.launched:
                    return JsonResponse(
                        {"success": False, "message": f"Cargo {cargo.cargoname} has already been launched."},
                        status=400)

            new_remaining_capacity = launch.remaining_capacity_kg

            with transaction.atomic():
                for booking in bookings_to_cancel:
                    print("about to cancel booking",booking)
                    Booking.objects.filter(id=booking.id).update(cancelled=True)
                    print("booking cancelled")
                    new_remaining_capacity += booking.cargo.total_weight()

                for cargo in cargo_to_book:
                    Booking.objects.create(
                        cargo=cargo,
                        launch=launch
                    )
                    new_remaining_capacity -= cargo.total_weight()

                if new_remaining_capacity < 0:
                    raise CapacityExceededError(f"Total cargo weight {new_remaining_capacity} exceeds the launch's remaining_capacity")

                Launch.objects.filter(id=launch.id).update(remaining_capacity_kg=new_remaining_capacity)

                return JsonResponse({"success":True,"message":"Booking successful! 🚀"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred while processing your booking: {e}"},status=500)

    
    # Fetch all cargo that matches the launch destination, including both booked and unbooked
    user_id = request.user.id
    cargo = Cargo.objects.filter(
        owner_id=user_id,
        launched=False,
        destination=launch.destination
    ).exclude(
        ~models.Q(id__in=Booking.objects.filter(cancelled=False, launch_id=launch.id).values_list('cargo_id', flat=True)) &
        models.Q(id__in=Booking.objects.filter(cancelled=False).values_list('cargo_id', flat=True))
    )

    # Mark booked cargo
    for c in cargo:
        c.booked = Booking.objects.filter(cargo=c, launch=launch, cancelled=False).exists()

    return render(request, "launches/make_booking.html", {"launch": launch, "cargo": cargo})