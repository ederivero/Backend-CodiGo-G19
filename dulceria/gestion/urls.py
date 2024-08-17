# Aca iran todas las rutas relacionadas a la aplicacion gestion
from django.urls import path
from .views import paginaPrueba

urlpatterns = [
    path('prueba', paginaPrueba)
]
