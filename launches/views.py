from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Launch, Rocket, Destination
from .forms import LaunchForm
from django.contrib import messages
# https://docs.google.com/document/d/1XGUq0u8KKOx4fce-acsl4qwd-HweDuUC6iR6hepofEU/edit?tab=t.0 review notes
def get_available_rockets(request):
    if request.method == "GET" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = LaunchForm(request.GET)

        if form.is_valid():
            destination_id = form.cleaned_data['destination'].id
            launch_date = form.cleaned_data['launch_date']
            result = fetch_available_rockets(destination_id, launch_date)
            available_rockets = result['available_rockets']
            required_range = result['required_range']
            destination = result['destination']
            launch_date = result['launch_date']
            return JsonResponse({ 'available_rockets': available_rockets, 'required_range': required_range, 'destination': destination, 'launch_date': launch_date }, safe=False)
        else:
            return JsonResponse({"error": "Invalid input"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def fetch_available_rockets(destination_id, launch_date, owner_id=2):
    try:
        destination = Destination.objects.get(id=destination_id)
        rockets = Rocket.objects.filter(owner_id=owner_id)
        available_rockets = []

        required_range = destination.distance * 2 * 1.1

        for rocket in rockets:
            if rocket.range_au >= required_range and not Launch.objects.filter(rocket=rocket,
                                                                            launch_date=launch_date).exists():
                cost = calculate_launch_cost(destination.distance, rocket.fuel_consumption_rate, rocket.fuel_cost)
                available_rockets.append({
                    'id': rocket.id,
                    'name': rocket.name,
                    'cost': cost,
                    'capacity': rocket.cargo_capacity_kg
                })

        return { 'available_rockets': available_rockets, 'required_range': required_range, 'destination': destination.name, 'launch_date': launch_date }
    except Destination.DoesNotExist:
        return { 'available_rockets': [], 'required_range': None, 'destination': None, 'launch_date': None }

def calculate_launch_cost(distance, fuel_consumption, fuel_cost):
    return round(distance * 2 * float(fuel_consumption) * float(fuel_cost),2)

# REPLACE 2 WITH THE USER_ID IN SESSION
def view_launches(request):
    """View all launches for a specific rocket owner"""
    launches = Launch.objects.filter(rocket__owner_id=2)
    return render(request, "launches/view_launches.html", {"launches": launches})

def view_all_launches(request):
    """View all launches"""
    launches = Launch.objects.all()
    return render(request, "launches/view_all_launches.html", {"launches": launches})

def add_launch(request):
    """Add a new launch"""
    if request.method == "POST":
        form = LaunchForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Launch successfully scheduled!")
                return redirect("view_all_launches")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = LaunchForm()
    return render(request, "launches/add_launch.html", {"form": form})

def edit_launch(request, id):
    """Edit a launch"""
    launch = get_object_or_404(Launch, id=id)
    if request.method == "POST":
        form = LaunchForm(request.POST, instance=launch)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Launch updated successfully!")
                return redirect("view_all_launches")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = LaunchForm(instance=launch)
    return render(request, "launches/edit_launch.html", {"form": form, "launch": launch})

def delete_rocket(request, id):
    """Delete a rocket"""
    rocket = get_object_or_404(Rocket, id=id)
    rocket.delete()
    messages.success(request, "Rocket successfully deleted!")
    return redirect("view_all_launches")
