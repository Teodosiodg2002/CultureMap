# lugares/forms.py

from django import forms
from .models import Lugar
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ['nombre', 'descripcion', 'direccion', 'lat', 'lng', 'categoria']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mirador de San Nicolás'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el lugar, su historia, por qué es especial...'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: C. Escuelas, 6, Granada, España'}),
            'lat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 37.1812'}),
            'lng': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: -3.5932'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        """
        Esto es para añadir las clases de Bootstrap a los campos
        automáticamente, igual que hicimos en LugarForm.
        """
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'tu-email@ejemplo.com'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirma tu contraseña'