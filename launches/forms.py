from django import forms
from .models import Launch, Rocket, Destination
from django.utils import timezone
from datetime import timedelta

class LaunchForm(forms.ModelForm):
    class Meta:
        model = Launch
        fields = ['launch_date', 'destination']  # Initial visible fields

    # We'll add other fields dynamically later
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rocket'] = forms.ModelChoiceField(
            queryset=Rocket.objects.none(),  # Initially, no rockets available
            required=True
        )
        self.fields['price_per_kg'] = forms.FloatField(
            min_value=0,
            required=True
        )
        min_date = timezone.now().date() + timedelta(weeks=1)
        self.fields['launch_date'] = forms.DateField(
            widget=forms.DateInput(attrs={
                'type': 'date',
                'min': min_date  # Prevent users from selecting a date earlier than 1 week ahead
            }),
            required=True,
        )