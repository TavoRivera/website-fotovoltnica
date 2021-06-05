from django.shortcuts import render

# Create your views here.
def index(request):
    # verifica si el usuario está logueado
    return render(request, "inventario/layout.html")
