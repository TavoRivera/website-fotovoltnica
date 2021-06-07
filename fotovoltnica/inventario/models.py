from django.db import models

# Create your models here.

#servicios
class Servicio(models.Model):
    name = models.CharField(max_length=42, blank=False)
    image = models.ImageField(upload_to="static/images/services/", blank=True)
    comment = models.CharField(max_length=120, blank=True)

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

class Capacidad(models.Model):
    capacity = models.CharField(max_length=18, blank=True)

    def __str__(self):
        return f"{self.capacity}"
