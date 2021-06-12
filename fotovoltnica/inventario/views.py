from datetime import datetime
from time import localtime, asctime
from django.shortcuts import render,  redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
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
        return render(request, "inventario/login.html", {"message_alert": "Para cotizar primero debes iniciar sesión"})
    precio = request.POST['amount']
    sistema = request.POST['selection']
    nombre = request.user.first_name
    apellido = request.user.last_name
    email = request.user.email
    articulos = request.POST.getlist("articulos")
    tiempo = datetime.now()

    asunto = "Cotización de un sistema de {}".format(sistema)

    datos_iniciales = "<h3><u>FOTOVOLTNICA</u></h3>\
                    <h5>RUC: 1234567890 </h5>\
                    <h5> Fecha: {} </h5>".format(tiempo)

    datos_cliente = "<h4><u>Datos del cliente:</u></h4>\
                    <p><b>Nombre:</b> {} {} </p>\
                    <p><b>Correo:</b> {} </p>\
                    <br><br>".format(nombre,apellido,email)

    mensaje = datos_iniciales + datos_cliente + "<h4><u>Detalles de la cotización:</u></h4>"

    mensaje = mensaje + "<p>Sistema: {} </p><p>Artículos que contiene: {} </p><p><b>Precio: {} </b></p> ".format(sistema,articulos,precio)
    mensaje = "<font face = 'Consolas, Courier, monospace'>" + mensaje + "</font>"
    correo = EmailMessage(subject=asunto, body = mensaje, to = [settings.EMAIL_HOST_USER, email])
    correo.fail_silently = False
    correo.content_subtype = "html"
    correo.send()
    messages.success(request, "Cotización exitosa. Nos pondremos en contacto con usted pronto")
    return redirect('index')

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST["name"]
        email = request.POST["email"]
        mensaje = request.POST["email"]

        asunto = "Consulta de {}".format(nombre)

        mensaje = mensaje + f"Remitente: {nombre}" + f"Contacto:{email}"

        correo = EmailMessage(subject=asunto, body= mensaje, to = [settings.EMAIL_HOST_USER])
        correo.fail_silently = False
        correo.send()
        messages.success(request, "Gracias por ponerte en contacto con nosotros, te responderemos lo más pronto posible")
        return redirect('index')


    return render(request, "inventario/contact.html")

def login_view(request):
    if request.method == 'GET':
        return render(request, 'inventario/login.html')
    try:
        username = request.POST['username']
        password = request.POST['password']

    except KeyError:
        return render(request, "inventario/login.html", {"message_alert": "Entrada inválida"})
    if not username:
        return render(request, "inventario/login.html", {"message_alert": "Usuario inválido"})
    if not password:
        return render(request, "inventario/login.html", {"message_alert": "Contraseña inválida"})

    user = authenticate(request, username=username, password=password)
    if not user:
        return render(request, 'inventario/login.html', {'message_alert': 'Credenciales inválidas'})
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
    messages.success(request, f" Gracias por registrarte")
    #return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))
