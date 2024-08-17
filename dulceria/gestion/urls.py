# Aca iran todas las rutas relacionadas a la aplicacion gestion
from django.urls import path
from .views import paginaPrueba, CategoriasAPIView, CrearCategoriaAPIView

urlpatterns = [
    path('prueba', paginaPrueba),
    path('categorias', CategoriasAPIView.as_view()),
    path('crear-categoria', CrearCategoriaAPIView.as_view()),
]
