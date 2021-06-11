from django.shortcuts import render,  redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from djngo.core.mail import EmailMessage
# from django.template.loader import render_to_string
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
    if not request.user.is_authenticated:
        return render(request, "inventario/login.html")
    precio = request.POST['amount']
    sistema = request.POST['selection']
    nombre = request.user.first_name
    apellido = request.user.last_name
    email = request.user.email

    datos_cliente = "<h4><u>Datos del cliente:</u></h4>\
                    <p><b>Nombre:</b> {} {} </p>\
                    <p><b>Correo:</b> {} </p>\
                    <br><br>".format(nombre,apellido,email)

    print(datos_cliente)



    return redirect('index')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'inventario/login.html')
    try:
        username = request.POST['username']
        password = request.POST['password']

    except KeyError:
        return render(request, "inventario/login.html", {"message_alert": "Invalid Entry"})
    if not username:
        return render(request, "inventario/login.html", {"message_alert": "Invalid Username"})
    if not password:
        return render(request, "inventario/login.html", {"message_alert": "Invalid Password"})

    user = authenticate(request, username=username, password=password)
    if not user:
        return render(request, 'inventario/login.html', {'message_alert': 'Invalid credentials'})
    else:
        login(request, user)
        # render(request, "orders/index.html", {"message_success": "Welcome!"})
        return HttpResponseRedirect(reverse('index'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


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
    return HttpResponseRedirect(reverse('index'))
