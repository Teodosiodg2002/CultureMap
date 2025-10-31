# lugares/forms.py

from django import forms
from .models import Lugar

class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ['nombre', 'descripcion', 'direccion', 'lat', 'lng', 'categoria']
        
        # (Opcional) Personaliza cómo se ven los campos
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mirador de San Nicolás'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el lugar, su historia, por qué es especial...'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: C. Marqués de Falces, 1'}),
            'lat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 37.1812'}),
            'lng': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: -3.5932'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }