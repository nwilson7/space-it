from .models import Destination, Rocket, Launch
from django.http import JsonResponse
from datetime import datetime
from users.models import User

def get_available_rockets(request):
    print("get_available_rockets successfully run!!")
    if request.method == "GET" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print("request.method == GET and request.headers.get('X-Requested-With') == XMLHttpRequest SUCCESS")
        print("request.GET: ", request.GET)

        # Manually get the parameters from the GET request
        destination_id = request.GET.get('destination')
        launch_date = request.GET.get('launch_date')

        # Check if both parameters are present
        if not destination_id or not launch_date:
            return JsonResponse({"error": "Missing parameters"}, status=400)

        try:
            # Convert destination_id to an integer and parse launch_date to a proper date format
            destination_id = int(destination_id)
            launch_date = datetime.strptime(launch_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format or destination ID"}, status=400)

        # Call the function to fetch available rockets
        result = fetch_available_rockets(request,destination_id, launch_date)
        available_rockets = result['available_rockets']
        required_range = result['required_range']
        destination = result['destination']
        launch_date = result['launch_date']

        # Return the available rockets as a JsonResponse
        return JsonResponse({
            'available_rockets': available_rockets,
            'required_range': required_range,
            'destination': destination,
            'launch_date': launch_date
        }, safe=False)

    return JsonResponse({"error": "Invalid request"}, status=400)

def fetch_available_rockets(request,destination_id, launch_date):
    try:
        user_id = request.user.id  
        destination = Destination.objects.get(id=destination_id)
        rockets = Rocket.objects.filter(owner_id=user_id)
        available_rockets = []
        print("rockets:",rockets)
        # Calculate the required range based on the destination's distance
        required_range = destination.distance * 2 * 1.1

        print("required range: ",required_range)

        # Check for available rockets
        for rocket in rockets:
            if rocket.range_au >= required_range and not Launch.objects.filter(rocket=rocket, launch_date=launch_date).exists():
                cost = calculate_launch_cost(destination.distance, rocket.fuel_consumption_rate, rocket.fuel_cost)
                available_rockets.append({
                    'id': rocket.id,
                    'name': rocket.name,
                    'cost': cost,
                    'capacity': rocket.cargo_capacity_kg,
                    'cost_per_kg': round(cost / rocket.cargo_capacity_kg, 2)
                })

        return {
            'available_rockets': available_rockets,
            'required_range': required_range,
            'destination': destination.name,
            'launch_date': launch_date
        }
    except Destination.DoesNotExist:
        return {
            'available_rockets': [],
            'required_range': None,
            'destination': None,
            'launch_date': None
        }

def calculate_launch_cost(distance, fuel_consumption, fuel_cost):
    return round(distance * 2 * float(fuel_consumption) * float(fuel_cost), 2)
