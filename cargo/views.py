# cargo/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cargo
from .forms import CargoForm
from users.models import User
from users.decorators import role_required

@role_required('cargo_owner')
def view_cargo(request):
    user_id = request.user.id  
    cargo_list = Cargo.objects.filter(owner_id=user_id)
    return render(request, 'cargo/cargo_list.html', {'cargo_list': cargo_list})

@role_required('cargo_owner')
def add_cargo(request):
    user_id = request.user.id 
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.owner=User.objects.get(id=user_id)
            cargo.save()
            return redirect('view_cargo')
    else:
        form = CargoForm()
    return render(request, 'cargo/add_cargo.html', {'form': form})

@role_required('cargo_owner')
def edit_cargo(request, id):
    user_id = request.user.id 
    cargo = get_object_or_404(Cargo, id=id)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.owner=User.objects.get(id=user_id)
            cargo.save()
            return redirect('view_cargo')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'cargo/edit_cargo.html', {'form': form, 'cargo': cargo})

@role_required('cargo_owner')
def delete_cargo(request, id):
    cargo = get_object_or_404(Cargo, id=id)
    cargo.delete()
    return redirect('view_cargo')