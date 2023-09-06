from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import comentario

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def menu(request):
    return render(request, 'core/menu.html')

#def login(request):
#    return render(request, 'core/login.html')

#def registro(request):
#    return render(request, 'core/registro.html')

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
    if request.method == 'GET':
        comentarios = comentario.objects.all()
        return render(request, 'products/producto.html', {'comentarios': comentarios})

    if request.method == 'POST':
        texto = request.POST['texto']
        comments = comentario(usuario=request.user, texto=texto)
        comments.save()
        return redirect('producto')

    return render(request, 'products/producto.html')
