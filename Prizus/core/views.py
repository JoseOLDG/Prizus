from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

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

#def login2(request):
    if request.method == 'GET':
        return render(request, 'registration2/login2.html', {'form': AuthenticationForm})

def login2(request):
    if request.method == 'GET':
        return render(request, 'registration2/login2.html', {
            "form": AuthenticationForm
            })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration2/login2.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('xd.html')