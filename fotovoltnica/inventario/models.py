from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.

#servicios
class Servicio(models.Model):
    name = models.CharField(max_length=42, blank=False)
    image = models.ImageField(upload_to="static/images/services/", blank=True)
    comment = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return f"{self.name}"

#Proyectos
class Proyecto(models.Model):
    name = models.CharField(max_length=42, blank=False)
    place =  models.CharField(max_length=32, blank=False)
    image = models.ImageField(upload_to="static/images/services/", blank=True)
    comment = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name} - {self.place}"


#aquí irán todos los productos: paneles, baterías, con su debida capacidad.
class Stock(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Sistema(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to="static/images/services", blank=True)
    items = models.ManyToManyField(
        Stock, blank=True, related_name="items")
    disponibility = models.BooleanField(default=False)
    system_type =  models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return f"{self.name}"

class PrecioSistema(models.Model):
    itemcost = models.ManyToManyField(
        Sistema, blank=True, related_name="cost")
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        for each in self.itemcost.all():
            return f"{each} ${self.amount}"
