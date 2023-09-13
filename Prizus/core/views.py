from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login

from .models import comentario

from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def menu(request):
    return render(request, 'core/menu.html')

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


def producto(request):
    """
    Esta vista carga la lista de comentarios, el 
    POST request es para cuando se escribe un comentario y
    el GET request para listarlos en el mismo html
    """
    
    comentarios = comentario.objects.all()

    if request.method == 'POST':
        texto = request.POST['texto']
        comments = comentario(usuario=request.user, texto=texto)
        comments.save()
        return redirect('producto')

    return render(request, 'products/producto.html', {'comentarios': comentarios})

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
        return redirect('xd.html')
    else:
        return render(request, 'registration2/login2.html', {"form": AuthenticationForm(), "error": "You are not authorized to access this page."})

