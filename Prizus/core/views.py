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
from django.http import JsonResponse
from .models import Calificacion
from django.contrib.auth import logout
from django.shortcuts import redirect


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

def index(request):
    return render(request, 'core/index.html')

def menu(request):
    queryset = request.GET.get("buscar")
    genero = request.GET.get("filtro")
    contenido_neto = request.GET.get("filtro_contenido")
    fragancia = request.GET.get("filtro_fragancia")

    content = {
        'productos': producto.objects.all()
    }

    if genero:
        content['productos'] = content['productos'].filter(Q(genero__icontains=genero))

    if contenido_neto:
        rango_filtro = {
            "1": (25, 50),
            "2": (50, 100),
            "3": (100, 150),
            "4": (150, 200),
            "5": (200, 500),
            "6": (500, 1000)
        }

        if contenido_neto in rango_filtro:
            rango = rango_filtro[contenido_neto]
            productos = producto.objects.filter(
                contenido_neto__gte=rango[0],
                contenido_neto__lte=rango[1]
            )
            content['productos'] = content['productos'].filter(pk__in=productos)

    if queryset:
        productos = producto.objects.filter(
            Q(nombre__icontains=queryset) | Q(descripcion__icontains=queryset) | Q(genero__icontains=queryset) | Q(contenido_neto__icontains=queryset) | Q(familia_olfativa__icontains=queryset) | Q(notas_salida__icontains=queryset) | Q(notas_corazon__icontains=queryset) | Q(notas_fondo__icontains=queryset)
        ).distinct()
        content['productos'] = content['productos'].filter(pk__in=productos)

    # Nueva sección para filtrar por fragancia seleccionada
    if fragancia:
        if fragancia == "7":  # Cítrica
            content['productos'] = content['productos'].filter(
                Q(nombre__icontains="Piña") | Q(descripcion__icontains="Piña") |
                Q(familia_olfativa__icontains="Piña") |
                Q(notas_salida__icontains="Piña") | Q(notas_corazon__icontains="Piña") | Q(notas_fondo__icontains="Piña") |
                Q(nombre__icontains="Naranja") | Q(descripcion__icontains="Naranja") |
                Q(familia_olfativa__icontains="Naranja") |
                Q(notas_salida__icontains="Naranja") | Q(notas_corazon__icontains="Naranja") | Q(notas_fondo__icontains="Naranja") |
                Q(nombre__icontains="limón") | Q(descripcion__icontains="limón") |
                Q(familia_olfativa__icontains="limón") |
                Q(notas_salida__icontains="limón") | Q(notas_corazon__icontains="limón") | Q(notas_fondo__icontains="limón") 
                
                
            )
        elif fragancia == "8":  # Aromática
            content['productos'] = content['productos'].filter(
                Q(nombre__icontains="lavanda") | Q(descripcion__icontains="lavanda") |
                Q(familia_olfativa__icontains="lavanda") |
                Q(notas_salida__icontains="lavanda") | Q(notas_corazon__icontains="lavanda") | Q(notas_fondo__icontains="lavanda") |
                Q(nombre__icontains="romero") | Q(descripcion__icontains="romero") |
                Q(familia_olfativa__icontains="romero") |
                Q(notas_salida__icontains="romero") | Q(notas_corazon__icontains="romero") | Q(notas_fondo__icontains="romero") |
                Q(nombre__icontains="salvia") | Q(descripcion__icontains="salvia") |
                Q(familia_olfativa__icontains="salvia") |
                Q(notas_salida__icontains="salvia") | Q(notas_corazon__icontains="salvia") | Q(notas_fondo__icontains="salvia") 
            )
        elif fragancia == "9":  # Frutal
            content['productos'] = content['productos'].filter(
                Q(nombre__icontains="manzana") | Q(descripcion__icontains="manzana") |
                Q(familia_olfativa__icontains="manzana") |
                Q(notas_salida__icontains="manzana") | Q(notas_corazon__icontains="manzana") | Q(notas_fondo__icontains="manzana") |
                Q(nombre__icontains="pera") | Q(descripcion__icontains="pera") |
                Q(familia_olfativa__icontains="pera") |
                Q(notas_salida__icontains="pera") | Q(notas_corazon__icontains="pera") | Q(notas_fondo__icontains="pera") |
                Q(nombre__icontains="melocotón") | Q(descripcion__icontains="melocotón") |
                Q(familia_olfativa__icontains="melocotón") |
                Q(notas_salida__icontains="melocotón") | Q(notas_corazon__icontains="melocotón") | Q(notas_fondo__icontains="melocotón") |
                Q(nombre__icontains="fresa") | Q(descripcion__icontains="fresa") |
                Q(familia_olfativa__icontains="fresa") |
                Q(notas_salida__icontains="fresa") | Q(notas_corazon__icontains="fresa") | Q(notas_fondo__icontains="fresa") |
                Q(nombre__icontains="Piña") | Q(descripcion__icontains="Piña") |
                Q(familia_olfativa__icontains="Piña") |
                Q(notas_salida__icontains="Piña") | Q(notas_corazon__icontains="Piña") | Q(notas_fondo__icontains="Piña")
            )
        elif fragancia == "10":  # Especiada
            content['productos'] = content['productos'].filter(
                Q(nombre__icontains="canela") | Q(descripcion__icontains="canela") |
                Q(familia_olfativa__icontains="canela") |
                Q(notas_salida__icontains="canela") | Q(notas_corazon__icontains="canela") | Q(notas_fondo__icontains="canela") |
                Q(nombre__icontains="clavo") | Q(descripcion__icontains="clavo") |
                Q(familia_olfativa__icontains="clavo") |
                Q(notas_salida__icontains="clavo") | Q(notas_corazon__icontains="clavo") | Q(notas_fondo__icontains="clavo") |
                Q(nombre__icontains="pimienta") | Q(descripcion__icontains="pimienta") |
                Q(familia_olfativa__icontains="pimienta") |
                Q(notas_salida__icontains="pimienta") | Q(notas_corazon__icontains="pimienta") | Q(notas_fondo__icontains="pimienta") |
                Q(nombre__icontains="nuez moscada") | Q(descripcion__icontains="nuez moscada") |
                Q(familia_olfativa__icontains="nuez moscada") |
                Q(notas_salida__icontains="nuez moscada") | Q(notas_corazon__icontains="nuez moscada") | Q(notas_fondo__icontains="nuez moscada")
            )

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
    
def guardar_puntuacion(request):
    if request.method == 'POST':
        puntuacion = int(request.POST.get('puntuacion'))

        calificacion = Calificacion(puntuacion=puntuacion)
        calificacion.save()

        return JsonResponse({'message': f'Calificación guardada: {puntuacion} estrellas.'})

    return JsonResponse({'error': 'Este endpoint solo admite solicitudes POST.'})


def obtener_productos_por_genero(request):
    genero = request.GET.get('genero', None)
    
    if genero is not None:
        # Realiza una consulta en la base de datos para obtener los productos filtrados por el género seleccionado
        productos_filtrados = Producto.objects.filter(descripcion=genero)
        
        # Convierte los productos en un formato JSON
        productos_json = [{'nombre': producto.nombre, 'imagen': producto.imagen, 'descripcion': producto.descripcion, 'slug': producto.slug} for producto in productos_filtrados]
        
        return JsonResponse(productos_json, safe=False)
    
    return JsonResponse([], safe=False)

def logout_view(request):
    logout(request)
    return redirect('nombre_de_la_página_de_inicio')

