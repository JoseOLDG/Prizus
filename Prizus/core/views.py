from pdb import post_mortem
from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import comentario, producto, precio
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import JsonResponse

from bs4 import BeautifulSoup
import requests


def extraer_informacion_perfume(url, tag_html_perfume, clase_precio_perfume):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      try:
        soup = BeautifulSoup(response.text, 'html.parser')

        precio_perfume = soup.find(name=f'{tag_html_perfume}', class_=f'{clase_precio_perfume}')

        try:
          clear_precio = int(''.join(filter(str.isalnum, precio_perfume.text.strip().encode("utf-8").decode("utf-8", "ignore"))))
        except:
          clear_precio = precio_perfume.text.strip()
        return clear_precio
      except:
        return print("Error en la extracción")
    else:
      return print("Error, codigo de estado: ", response.status_code)
  except:
    return print("Error en la solicitud")

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def menu(request):
    queryset = request.GET.get("buscar")
    print("Valor de queryset:", queryset)  # Agregar esta línea para depuración
    content = {
        'productos': producto.objects.all()
    }
    if queryset:
        productos = producto.objects.filter(
            Q(nombre__icontains=queryset) | Q(descripcion__icontains=queryset) | Q(genero__icontains=queryset) | Q(contenido_neto__icontains=queryset) | Q(familia_olfativa__icontains=queryset) | Q(notas_salida__icontains=queryset) | Q(notas_corazon__icontains=queryset) | Q(notas_fondo__icontains=queryset)
        ).distinct()
        print("Resultados de la consulta:", productos)  # Agregar esta línea para depuración
        content['productos'] = productos 

    return render(request, 'core/menu.html', content)

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request,user)
            return redirect(to="index")
        data["form"] = formulario
        
    
    return render(request, 'registration/registro.html', data)

def perfumes(request, slug):
    comentarios = comentario.objects.all()
    perfume = get_object_or_404(producto, slug=slug)

    if request.method == 'POST':
        try:
            texto = request.POST['texto']
            comments = comentario(usuario=request.user, texto=texto)
            comments.save()
            return redirect('producto')
        except:
            return redirect('login')

    content = {
        'comentarios': comentarios,
        'producto': perfume,
    }

    return render(request, 'products/producto.html', content)

def update_prices(request, slug):
    valores = precio.objects.filter(producto__slug__icontains=slug)

    updated_prices = []

    for val in valores:
        nuevo_valor = extraer_informacion_perfume(val.webScraping_url, val.tienda.webScraping_tag, val.tienda.webScraping_precio)
        tienda_valor = val.tienda.nombre
        val.save()
        updated_prices.append([nuevo_valor, tienda_valor])

    return JsonResponse({'prices': updated_prices})

def login2(request):
    if request.method == 'GET':
        return render(request, 'registration2/login2.html', {"form": AuthenticationForm()})

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, 'registration2/login2.html', {"form": AuthenticationForm(), "error": "Username or password is incorrect."})

    if user.is_staff:
        login(request, user)
        return redirect('admin:index')
    else:
        return render(request, 'registration2/login2.html', {"form": AuthenticationForm(), "error": "You are not authorized to access this page."})

def obtener_productos_por_genero(request):
    genero = request.GET.get('genero', None)
    
    if genero is not None:
        # Realiza una consulta en la base de datos para obtener los productos filtrados por el género seleccionado
        productos_filtrados = Producto.objects.filter(descripcion=genero)
        
        # Convierte los productos en un formato JSON
        productos_json = [{'nombre': producto.nombre, 'imagen': producto.imagen, 'descripcion': producto.descripcion, 'slug': producto.slug} for producto in productos_filtrados]
        
        return JsonResponse(productos_json, safe=False)
    
    return JsonResponse([], safe=False)
