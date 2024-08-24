from django.urls import path
from .views import crearUsuario, perfilUsuario, ListaNoviosAPIView, generarCloudinaryUrl
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('registro', crearUsuario),
    path('login', TokenObtainPairView.as_view()),
    path('perfil', perfilUsuario),
    path('lista-novios', ListaNoviosAPIView.as_view()),
    path('cloudinary-url', generarCloudinaryUrl)
]
