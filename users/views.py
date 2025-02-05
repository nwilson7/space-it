from django.shortcuts import render, redirect # get_object_or_404 to be added here when used
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomLoginForm, UserEditForm
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request,"users/index.html",{})


def signup_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # Redirect to login after signup
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after successful login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomLoginForm()

    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login')

@login_required
def edit_user(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)  # Pass user instance to form
        password_form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            form.save()  # Save updated user details
            messages.success(request, "Your profile has been updated.")

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, "Your password has been updated.")

        return redirect('edit_user')  # Redirect back to edit page

    else:
        form = UserEditForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'users/edituser.html', {'form': form, 'password_form': password_form})

'''
def delete_rocket_owner(request, user_id):
    user = get_object_or_404(User, id=user_id, role='rocket_owner')

    # Step 1: Check if the user has any launches
    if Launch.objects.filter(rocket__owner=user).exists():
        messages.error(request, "Cannot delete user: Active launches exist.")
        return redirect('view_users')

    with transaction.atomic():  # Ensure all changes are made together
        # Step 2: Remove foreign key constraints from Rocket
        Rocket.objects.filter(owner=user).update(owner=None)

        # Step 3: Remove foreign key constraints from Transactions
        Transaction.objects.filter(sender=user).update(sender=None)
        Transaction.objects.filter(recipient=user).update(recipient=None)

        # Step 4: Delete rockets that are NOT booked & have no upcoming launches
        rockets_to_delete = Rocket.objects.filter(
            owner=user
        ).exclude(launch__launch_date__gte=timezone.now())  # Exclude rockets with future launches

        for rocket in rockets_to_delete:
            Launch.objects.filter(rocket=rocket).update(rocket=None)  # Remove FK constraints
            rocket.delete()

        # Step 5: Delete the user
        user.delete()
        messages.success(request, "Rocket owner deleted successfully.")

    return redirect('view_users')

def delete_cargo_owner(request, user_id):
    user = get_object_or_404(User, id=user_id, role='cargo_owner')

    with transaction.atomic():
        # Step 1: Remove foreign key constraints from Transactions
        Transaction.objects.filter(sender=user).update(sender=None)
        Transaction.objects.filter(recipient=user).update(recipient=None)

        # Step 2: Cancel cancellable bookings (assuming there's a `cancel` method)
        for booking in Booking.objects.filter(cargo__owner=user):
            if booking.can_be_cancelled():  # Implement logic for cancellability
                booking.cancel()
            booking.launch = None  # Remove FK
            booking.save()

        # Step 3: Remove foreign key constraints from Bookings
        Booking.objects.filter(cargo__owner=user).update(cargo=None)

        # Step 4: Delete deletable cargo
        Cargo.objects.filter(owner=user).delete()

        # Step 5: Delete the user
        user.delete()
        messages.success(request, "Cargo owner deleted successfully.")

    return redirect('view_users')
'''