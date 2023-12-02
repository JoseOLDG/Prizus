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
            'nombre',
            'webScraping_tag',
            'webScraping_precio',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'solo-leer'})
        }

class PrecioForm(forms.ModelForm):
    class Meta:
        model = precio
        fields = [
            'producto',
            'webScraping_url',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'producto' in self.fields:
            opciones = producto.objects.all().values_list('nombre', flat=True)
            self.fields['producto'].queryset = opciones
        self.fields['webScraping_url'].widget.attrs.update({'class': 'form-control'})
