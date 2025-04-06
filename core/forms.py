from django import forms
from .models import Pelada

class PeladaForm(forms.ModelForm):
    class Meta:
        model = Pelada
        fields = ['nome', 'data', 'local']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }