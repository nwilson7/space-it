from django.shortcuts import render, redirect # get_object_or_404 to be added here when used
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomLoginForm, UsernameUpdateForm, EmailUpdateForm
from django.contrib import messages
from .models import User
from .decorators import logout_required, login_required

# Create your views here.
@login_required
def index(request):
    return render(request,"users/index.html",{})

@logout_required
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

@logout_required
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

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login')

@login_required
def edit_user(request):
    user = request.user

    if request.method == 'POST':
        if 'update_username' in request.POST:  # Username form submitted
            username_form = UsernameUpdateForm(request.POST, instance=user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Your username has been updated.")
                return redirect('home')

        elif 'update_email' in request.POST:  # Email form submitted
            email_form = EmailUpdateForm(request.POST, instance=user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Your email has been updated.")
                return redirect('home')

        elif 'change_password' in request.POST:  # Password form submitted
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been updated.")
                return redirect('home')
            else:
                messages.error(request, "Please correct the error below.")

    else:
        username_form = UsernameUpdateForm(instance=user)
        email_form = EmailUpdateForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'users/edituser.html', {
        'username_form': username_form,
        'email_form': email_form,
        'password_form': password_form,
    })
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