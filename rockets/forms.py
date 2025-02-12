from django import forms
from .models import Rocket

class RocketForm(forms.ModelForm):
    class Meta:
        model = Rocket
        fields = ['name', 'cargo_capacity_kg', 'fuel_consumption_rate', 'fuel_cost', 'fuel_capacity']