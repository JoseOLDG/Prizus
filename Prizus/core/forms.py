from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import producto, tiendaOnline, precio

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
        widgets = {
            'descripcion': forms.Textarea(attrs={"rows":"5"}),
            'notas_salida': forms.Textarea(attrs={"rows":"3"}),
            'notas_corazon': forms.Textarea(attrs={"rows":"3"}),
            'notas_fondo': forms.Textarea(attrs={"rows":"3"}),
        }


class TiendaForm(forms.ModelForm):
    class Meta:
        model = tiendaOnline
        fields = [
            'webScraping_tag',
            'webScraping_precio',
        ]

class PrecioForm(forms.ModelForm):
    class Meta:
        model = precio
        try:
            opciones = producto.objects.all().values('nombre') 
        except:
            opciones = (("", ""),)
        fields = [
            'producto',
            'webScraping_url',
        ]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}, choices=opciones),
            'webScraping_url': forms.TextInput(attrs={'class': 'form-control'}),
        }