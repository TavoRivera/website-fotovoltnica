from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register', views.register, name='register'),
    path('systems', views.systems, name='systems'),
    path('cotizar', views.cotizar, name='cotizar'),
]
