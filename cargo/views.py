# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cargo
from .forms import CargoForm
from users.models import User

def view_cargo(request):
    cargo_list = Cargo.objects.filter(owner_id=1)
    return render(request, 'myapp/cargo_list.html', {'cargo_list': cargo_list})

def add_cargo(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.owner=User.objects.get(id=1)
            cargo.save()
            return redirect('view_cargo')
    else:
        form = CargoForm()
    return render(request, 'myapp/add_cargo.html', {'form': form})

def edit_cargo(request, id):
    cargo = get_object_or_404(Cargo, id=id)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.owner=User.objects.get(id=1)
            cargo.save()
            return redirect('view_cargo')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'myapp/edit_cargo.html', {'form': form, 'cargo': cargo})

def delete_cargo(request, id):
    cargo = get_object_or_404(Cargo, id=id)
    cargo.delete()
    return redirect('view_cargo')

def launch_cargo(request, id):
    cargo = get_object_or_404(Cargo, id=id)
    cargo.launched = True
    cargo.save()
    return redirect('view_cargo')
