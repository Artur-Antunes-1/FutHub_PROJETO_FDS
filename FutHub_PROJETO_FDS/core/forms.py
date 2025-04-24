from django import forms
from .models import Pelada

class PeladaForm(forms.ModelForm):
    recorrente = forms.BooleanField(
        required=False,
        label='Pelada semanal',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Pelada
        fields = ['nome', 'data_inicial', 'hora', 'local', 'recorrente']
        widgets = {
            'data_inicial': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da pelada'
            }),
            'local': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local do jogo'
            }),
        }
