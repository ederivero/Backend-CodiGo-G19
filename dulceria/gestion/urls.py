# Aca iran todas las rutas relacionadas a la aplicacion gestion
from django.urls import path
from .views import (paginaPrueba,
                    CategoriasAPIView,
                    CrearCategoriaAPIView,
                    CrearYListarCategoriaAPIView,
                    DevolverActualizarEliminarCategoriaAPIView,
                    GolosinasAPIView)

urlpatterns = [
    path('prueba', paginaPrueba),
    path('categorias', CategoriasAPIView.as_view()),
    path('crear-categoria', CrearCategoriaAPIView.as_view()),
    path('listar-crear-categoria', CrearYListarCategoriaAPIView.as_view()),
    # una vista generica que sea Retrieve | Update | Destroy o la combinacion de ellas
    path('categoria/<id>', DevolverActualizarEliminarCategoriaAPIView.as_view()),
    path('golosinas', GolosinasAPIView.as_view()),
]
