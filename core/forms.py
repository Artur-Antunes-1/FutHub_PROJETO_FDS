from django import forms
from .models import Pelada

class PeladaForm(forms.ModelForm):
    class Meta:
        model = Pelada
        fields = ['nome', 'data', 'local']
        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'dd/mm/aaaa'
            }),
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome da pelada'
            }),
            'local': forms.TextInput(attrs={
                'placeholder': 'Local do jogo'
            })
        }
        labels = {
            'nome': 'Nome da Pelada',
            'data': 'Data do Jogo',
            'local': 'Local'
        }