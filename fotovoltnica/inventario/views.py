from django.shortcuts import render,  redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import *

# Create your views here.
def index(request):

    context = {
        'servicios': Servicio.objects.all(),
        'proyectos': Proyecto.objects.all()
    }
    return render(request, "inventario/index.html", context)

def systems(request):
    context = {
        'servicios': Servicio.objects.all(),
        'sistemas': Sistema.objects.all(),
        'articulos': Stock.objects.all()
    }
    return render(request, "inventario/systems.html", context)

def cotizar(request):
    precio = request.POST['amount']
    print(precio)

    return redirect('index')


# def register(request):
#     form = SignUpForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         first = form.cleaned_data.get('first')
#         last = form.cleaned_data.get('last')
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, first=first, last=last, email=email, password=password)
#         login(request, user)
#         return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'inventario/register.html', {'form': form})


def register(request):
    if request.method == 'GET':
        return render(request, 'inventario/register.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]

    except KeyError:
        return render(request, "inventario/register.html", {"message_alert": "Entrada inválida"})
    if not username:
        return render(request, "inventario/register.html", {"message_alert": "Nombre de Usuario inválido"})
    if not password:
        return render(request, "inventario/register.html", {"message_alert": "Contraseña inválida"})

    check_user = User.objects.filter(username=username)
    if check_user:
        return render(request, "inventario/register.html", {"message_alert": "Ese nombre de usuario ya existe, por favor intente con otro"})
    if User.objects.filter(email=email).exists():
        return render(request, "inventario/register.html", {"message_alert": "Ese email ya está en uso, por favor intente con otor"})
    if len(first_name) < 2:
        return render(request, "inventario/register.html", {"message_alert": "Escriba su nombre completo"})
    if len(last_name) < 2:
        return render(request, "inventario/register.html", {"message_alert": "Escriba su apellido completo"})

    user = User.objects.create_user(
        username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    user.save()
    login(request, user)

    # return redirect(request.get_full_path())
    # messages.success(request, f" Now you're registered!")
    #return HttpResponseRedirect(reverse('index'))
    return render(request, "inventario/index.html")
