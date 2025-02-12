from django.shortcuts import render, get_object_or_404, redirect
from .models import Rocket
from .forms import RocketForm
from users.models import User
from django.contrib.auth.decorators import login_required
#from users.models import User  # Import the User model
# Create your views here.

# add an authorisation / authentication check

# GET OWNER WITH SESSION DATA
def view_rockets(request):
    user_id = request.user.id
    rockets = Rocket.objects.filter(owner_id=user_id)
    return render(request, "rockets/view_rockets.html", {'rockets': rockets})
# UPDATE SO THAT ROCKET.OWNER IS TAKEN FROM SESSION
def add_rocket(request):
    user_id = request.user.id
    if request.method == 'POST':
        form = RocketForm(request.POST)
        if form.is_valid():
            rocket = form.save(commit=False)  # Save the new rocket
            rocket.owner=User.objects.get(id=user_id)
            rocket.save()
            return redirect('view_rockets')  # Redirect to the list of rockets
    else:
        form = RocketForm()  # If it's a GET request, display an empty form

    return render(request, "rockets/add_rocket.html", {'form': form})

# UPDATE SO THAT ROCKET.OWNER IS TAKEN FROM SESSION
def edit_rocket(request, id):
    user_id = request.user.id
    # Get the rocket object to be edited
    rocket = get_object_or_404(Rocket, id=id, owner=request.user)

    # Check if the form was submitted
    if request.method == 'POST':
        form = RocketForm(request.POST, instance=rocket)
        if form.is_valid():
            rocket = form.save(commit=False)  # Save the new rocket
            rocket.owner=User.objects.get(id=user_id)
            rocket.save()
            return redirect('view_rockets')  # Redirect to the rockets list after saving
    else:
        form = RocketForm(instance=rocket)

    return render(request, 'rockets/edit_rocket.html', {'form': form, 'rocket': rocket})

def delete_rocket(request, id):
    # Get the rocket object to delete
    rocket = get_object_or_404(Rocket, id=id, owner=request.user)

    # ENSURE THE ROCKET IS NOT PART OF ANY UPCOMING LAUNCHES

    #if rocket.launch_set.filter(status='upcoming').exists():
     #  return redirect('view_rockets')   If it's part of an upcoming launch, don't delete

    # Delete the rocket
    rocket.delete()
    return redirect('view_rockets')
