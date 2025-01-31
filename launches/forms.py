from django import forms
from .models import Launch
from datetime import date, timedelta

class LaunchForm(forms.ModelForm):
    class Meta:
        model = Launch
        fields = ['launch_date', 'destination']
        widgets = {
            'launch_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the minimum date for launch_date to tomorrow
        tomorrow = date.today() + timedelta(days=1)
        self.fields['launch_date'].widget.attrs['min'] = tomorrow.strftime('%Y-%m-%d')
