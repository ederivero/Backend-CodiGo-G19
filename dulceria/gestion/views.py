from django.shortcuts import render
# El APIView sirve para definir en una clase todos los metodos HTTP que pueden ser consultados
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import Categoria
from .serializers import CategoriaSerializer


def paginaPrueba(request):
    print(request)
    data = [{
        "id": 1,
        "nombre": "Importados",
        "habilitado": True
    }, {
        "id": 2,
        "nombre": "Nacionales",
        "habilitado": False
    }]

    usuario = 'Eduardo'

    return render(request, 'prueba.html', {"data": data, "usuario": usuario})


class CategoriasAPIView(APIView):
    def get(self, request):
        return Response(data={
            'message': 'ok'
        }, status=200)

    def post(self, request):
        return Response(data={
            'message': 'me hiciste POST'
        }, status=200)


class CrearCategoriaAPIView(CreateAPIView):
    # https://www.django-rest-framework.org/api-guide/generic-views/#attributes
    # los atributos necesarios para utilizar una vista generica son:
    # SELECT * FROM categorias;
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
