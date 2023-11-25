from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import producto

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', "email", "password1", "password2"]

class ImagenForm(forms.Form):
    imagen = forms.FileField(label=False)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = producto
        fields = [
            'genero',
            'nombre',
            'descripcion',
            'marca',
            'contenido_neto',
            'familia_olfativa',
            'notas_salida',
            'notas_corazon',
            'notas_fondo',
            'imagen',
            'forma',
        ]
