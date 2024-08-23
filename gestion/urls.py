from django.urls import path
from .views import crearUsuario, perfilUsuario
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('registro', crearUsuario),
    path('login', TokenObtainPairView.as_view()),
    path('perfil', perfilUsuario),
]
