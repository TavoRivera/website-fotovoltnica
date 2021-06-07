from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *

# Create your views here.
def index(request):
    
    context = {
        'servicios': Servicio.objects.all(),
        'proyectos': Proyecto.objects.all()
    }
    return render(request, "inventario/layout.html", context)
