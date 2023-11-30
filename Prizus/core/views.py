from pdb import post_mortem
from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UserCreationForm, CustomUserCreationForm, ImagenForm, ProductoForm, TiendaForm, PrecioForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from .models import comentario, producto, precio, registroHistoricoPrecio, tiendaOnline

import numpy as np
import tensorflow as tf
import os
from django.conf import settings
import re
import openpyxl

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
    precios = precio.objects.filter(producto = perfume)
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
        'precio': precios
    }

    return render(request, 'products/producto.html', content)

def update_prices(request, id):
    valores = precio.objects.filter(tienda=id)
    tiendas = tiendaOnline.objects.filter(id=id)
    for t in tiendas:
        tienda = t.nombre
    try:
        for val in valores:
            try:
                nuevo_valor = extraer_informacion_perfume(val.webScraping_url, val.tienda.webScraping_tag, val.tienda.webScraping_precio)
                if val.valor != nuevo_valor:
                    val.valor = nuevo_valor
                    val.save()
                    registroHistoricoPrecio.objects.create(
                        producto=val.producto,
                        tienda = val.tienda,
                        precio_registrado=nuevo_valor,
                    )
            except:
                nuevo_valor = 0
                val.valor = nuevo_valor
                val.save()
                registroHistoricoPrecio.objects.create(
                    producto=val.producto,
                    tienda = val.tienda,
                    precio_registrado=nuevo_valor,
                )
        return redirect('actualizar_precios', nombre=tienda)
    except:
        return redirect('actualizar_precios', nombre=tienda)

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
                perfume_path = tf.keras.utils.get_file(f'Perfume: {imagen_name}', origin=perfume_url)
                
                img = tf.keras.utils.load_img(perfume_path, target_size=(img_height, img_width))
                img_array = tf.keras.utils.img_to_array(img)
                img_array_expand = tf.expand_dims(img_array, 0)

                predictions = model.predict(img_array_expand)
                score = tf.nn.softmax(predictions[0])
                os.remove(imagen_path)
            forma_predict = class_names[np.argmax(score)]
            productos = producto.objects.filter(forma__icontains=forma_predict)
            alerta = 'Analisis finalizado! Estos perfumes lucen semejantes con tu envase ingresado'
            print("Este perfume claramente tiene forma {} , mentira, es un porcentaje de {:.2f} de certeza.".format(class_names[np.argmax(score)], 100 * np.max(score)))    
            return render(request, 'core/menu.html', {'productos': productos, 'alerta': alerta})
            
    else:
        form = ImagenForm()
    return render(request, 'core/prizus_ia.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login2')
    return render(request, 'registration2/dashboard.html')

@login_required
def admin_perfumes(request):
    if not request.user.is_staff:
        return redirect('login2')
    
    content = {
        'productos': producto.objects.all()
    }
    
    if request.method=="POST":
        queryset = request.POST['search']
        if queryset:
            productos = producto.objects.filter(
                Q(id__icontains=queryset) | Q(nombre__icontains=queryset) | Q(descripcion__icontains=queryset) | Q(genero__icontains=queryset) | Q(contenido_neto__icontains=queryset) | Q(familia_olfativa__icontains=queryset) | Q(notas_salida__icontains=queryset) | Q(notas_corazon__icontains=queryset) | Q(notas_fondo__icontains=queryset) | Q(forma__icontains=queryset)
            ).distinct()
            content['productos'] = content['productos'].filter(pk__in=productos)

    return render(request, 'registration2/pages/perfumes.html', content)

@login_required
def admin_perfumes_detail(request, slug):
    if not request.user.is_staff:
        return redirect('login2')
    
    perfume = get_object_or_404(producto, slug=slug)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=perfume)
        if form.is_valid():
            form.save()
            return redirect('perfumes_detail', slug=perfume.slug)
    else: 
        form = ProductoForm(instance=perfume)

    content = {
        'perfume': perfume,
        'form': form
    }

    return render(request, 'registration2/pages/edit_perfume.html', content)

@login_required
def admin_precios(request):
    if not request.user.is_staff:
        return redirect('login2')
    
    content = {
        'tiendas': tiendaOnline.objects.all()
    }

    return render(request, 'registration2/pages/precios.html', content)

@login_required
def admin_precios_actualizar(request, nombre):
    if not request.user.is_staff:
        return redirect('login2')
    
    tienda = get_object_or_404(tiendaOnline, nombre=nombre)

    if request.method == 'POST':
        form = TiendaForm(request.POST, instance=tienda)
        if form.is_valid():
            form.save()
            return redirect('actualizar_precios', nombre=tienda.nombre)
    else: 
        form = TiendaForm(instance=tienda)
    
    
    precios = precio.objects.filter(tienda=tienda.id)
    list_product = producto.objects.all()

    content = {
        'tiendas': tienda,
        'productos': precios,
        'form': form,
        'PrecioForm': PrecioForm,
        'list_product': list_product
    }

    return render(request, 'registration2/pages/update_precios.html', content)

@login_required
def admin_tendencias(request):
    if not request.user.is_staff:
        return redirect('login2')
    return render(request, 'registration2/pages/tendencias.html')

@login_required
def new_prices(request, id): 
    if not request.user.is_staff:
        return redirect('login2')
    tiendas = tiendaOnline.objects.get(id=id)
    if request.method == 'POST':
        form = PrecioForm(request.POST)
        new_producto = producto.objects.get(nombre = form.data['producto'])
        url = form.data['webScraping_url']
        precio.objects.create(
            producto = new_producto,
            tienda = tiendas,
            webScraping_url = url,
        )
        return redirect('actualizar_precios', nombre=tiendas)
    else: 
        form = PrecioForm()
    return redirect('actualizar_precios', nombre=tiendas)


def generar_excel(request):
    productos_popularidad = producto.objects.all().values('id', 'nombre', 'views')
    lista_productos = list(productos_popularidad)
    # Abrimos el libro de excel
    workbook = openpyxl.Workbook()
    # Esto es para crear la hoja de tendencias con id ID | nombre Producto | views Número de vistas
    tendencias = workbook.active
    tendencias.title = 'Tendencias'
    tendencias['A1'] = 'ID'
    tendencias['B1'] = 'Producto'
    tendencias['C1'] = 'Número de vistas' 
    i = 1
    for lista in lista_productos:
        i = i + 1
        for key, value in lista.items():
            if key == 'id':
                print(f'A{i}: {value}')
                tendencias[f'A{i}'] = value
            if key == 'nombre':
                print(f'B{i}: {value}')
                tendencias[f'B{i}'] = value
            if key == 'views':
                print(f'C{i}: {value}')
                tendencias[f'C{i}'] = value


    # Crear el directorio "reports" en el proyecto Django si no existe
    directorio_reports = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    if not os.path.exists(directorio_reports):
        os.makedirs(directorio_reports)

    # Guardar el archivo de Excel en el directorio "media"
    archivo_excel_path = os.path.join(directorio_reports, 'archivo_excel.xlsx')
    workbook.save(archivo_excel_path)

    # Abrir el archivo y leer su contenido binario
    with open(archivo_excel_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={}'.format(escape_uri_path('archivo_excel.xlsx'))
    
    return response
