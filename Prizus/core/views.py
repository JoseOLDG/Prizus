from pdb import post_mortem
from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UserCreationForm, CustomUserCreationForm, ImagenForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.http import HttpResponse
from .models import comentario, producto, precio, registroHistoricoPrecio

import numpy as np
import tensorflow as tf
import os
from django.conf import settings
import re

from .models import comentario, producto, precio
from django.db.models import Q

from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import JsonResponse


from bs4 import BeautifulSoup
import requests
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def extraer_informacion_perfume(url, tag_html_perfume, clase_precio_perfume):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                elemento = soup.find(name=f'{tag_html_perfume}', class_=f'{clase_precio_perfume}')
                if elemento:
                    # Busca los precios dentro del texto del elemento
                    precios = [int(''.join(filter(str.isalnum, parte.encode("utf-8").decode("utf-8", "ignore"))) or '0')
                               for parte in elemento.stripped_strings]

                    if precios:
                        precio_minimo = min(precios)
                        return precio_minimo
                    else:
                        return "No se encontraron precios válidos en el texto del elemento"

                else:
                    return "No se encontró un elemento con la clase y etiqueta especificada"

            except:
                return "Error en la extracción"
        else:
            return f"Error, código de estado: {response.status_code}"
    except:
        return "Error en la solicitud"

def index(request):
    return render(request, 'core/index.html')

def menu(request):
    queryset = request.GET.get("buscar")
    genero = request.GET.get("filtro")
    contenido_neto = request.GET.get("filtro_contenido")

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
    perfume.views = perfume.views + 1
    perfume.save()

    if request.method == 'POST':
        texto = request.POST['texto']
        puntuacion = int(request.POST.get('puntuacion'))
        comments = comentario(producto=perfume, usuario=request.user, texto=texto, puntuacion=puntuacion)
        comments.save()
        return redirect('producto', slug=perfume.slug)

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
        producto_url = val.webScraping_url
        if val.valor != nuevo_valor:
            val.valor = nuevo_valor
            val.save()
            registroHistoricoPrecio.objects.create(
                producto=val.producto,
                tienda = val.tienda,
                precio_registrado=nuevo_valor,
            )
        updated_prices.append([nuevo_valor, tienda_valor, producto_url])

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
        return redirect('dashboard')
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

def logout_view(request):
    logout(request)
    return redirect('')

def procesar_imagen_ia(request):
    if request.method == 'POST':
        # Verifica si el campo de archivo se ha enviado y no está vacío
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.cleaned_data['imagen']

            s = imagen.name
            slug = re.sub(r'[^a-z0-9]+', '-', s).lower().strip('-')
            imagen_name = re.sub(r'[-]+', '-', slug).replace("-jpg", ".jpg")

            imagen_path = os.path.join(settings.MEDIA_ROOT, imagen_name)
            with open(os.path.join(settings.MEDIA_ROOT, imagen_name), 'wb') as destination:
                for chunk in imagen.chunks():
                    destination.write(chunk)
            # Procesa el formulario
            if os.path.exists(imagen_path):
                model = tf.keras.models.load_model("models/PrizusML.h5")

                img_height = 180
                img_width = 180

                class_names = ['Cilindro', 'Cintura', 'Cuadrado', 'Esfera', 'Figura', 'Pack', 'Prisma', 'Rectangulo', 'Tronco']

                perfume_url = f'http://127.0.0.1:8000{os.path.join(settings.MEDIA_URL, imagen_name)}'
                perfume_path = tf.keras.utils.get_file('Perfume: {imagen.name}', origin=perfume_url)
                
                img = tf.keras.utils.load_img(perfume_path, target_size=(img_height, img_width))
                img_array = tf.keras.utils.img_to_array(img)
                img_array_expand = tf.expand_dims(img_array, 0)

                predictions = model.predict(img_array_expand)
                score = tf.nn.softmax(predictions[0])
                os.remove(imagen_path)
            forma_predict = class_names[np.argmax(score)]
            productos = producto.objects.filter(forma__icontains=forma_predict)
            print("Este perfume claramente tiene forma {} , mentira, es un porcentaje de {:.2f} de certeza.".format(class_names[np.argmax(score)], 100 * np.max(score)))    
            return render(request, 'core/menu.html', {'productos': productos})
            
    else:
        form = ImagenForm()
    return render(request, 'core/prizus_ia.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login2')
    return render(request, 'registration2/dashboard.html')