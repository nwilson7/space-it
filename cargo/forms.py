# myapp/forms.py
from django import forms
from .models import Cargo

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['cargoname', 'weight_per_item', 'number_of_items', 'destination']
