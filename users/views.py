from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import CustomLoginForm

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