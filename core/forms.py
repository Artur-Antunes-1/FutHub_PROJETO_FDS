from django import forms
from .models import Pelada

class PeladaForm(forms.ModelForm):
    class Meta:
        model = Pelada
        fields = ['nome', 'data', 'hora', 'local']  
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),  
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da pelada'}),
            'local': forms.TextInput(attrs={'placeholder': 'Local do jogo'})
        }
        labels = {
            'nome': 'Nome da Pelada',
            'data': 'Data do Jogo',
            'hora': 'Horário',  
            'local': 'Local'
        }