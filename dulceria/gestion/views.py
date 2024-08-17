from django.shortcuts import render
# El APIView sirve para definir en una clase todos los metodos HTTP que pueden ser consultados
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Categoria, Golosina
from .serializers import CategoriaSerializer, GolosinaSerializer
from rest_framework import status


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


class CrearYListarCategoriaAPIView(ListCreateAPIView):
    # https://www.django-rest-framework.org/api-guide/generic-views/#attributes
    # los atributos necesarios para utilizar una vista generica son:
    # SELECT * FROM categorias;
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class DevolverActualizarEliminarCategoriaAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # Si queremos cambiar el valor del parametro por la url de pk a una personalizado usaremos el atributo lookup_field
    lookup_field = 'id'


class GolosinasAPIView(APIView):
    def post(self, request):
        # obtener la informacion del body del request
        data = request.data  # convierte a un dict

        serializador = GolosinaSerializer(data=data)

        # hace la validacion de los campos del body
        validacion = serializador.is_valid()

        if validacion:
            # en los serializadores se puede guardar en la base de datos directamente
            nuevaGolosinaCreada = serializador.save()

            # nuevaGolosina = Golosina(nombre=serializador.validated_data.get('nombre'),
            #                          precio=serializador.validated_data.get(
            #                              'precio'),
            #                          habilitado=serializador.validated_data.get(
            #                              'habilitado'),
            #                          categoria=serializador.validated_data.get('categoria'))
            # validated_data es la informacion YA VALIDADA, solamente se puede acceder a ella luego de llamar al metodo is_valid() (71) si no llamamos a este metodo e intentamos usar el validated_data entonces nos lanzara un error

            # Metodo sin serializador
            # nuevaGolosina = Golosina(**serializador.validated_data)
            # nuevaGolosina.save()

            # Si queremos validar que la informacion a guardar o actualizar es correcta usaremos el parametro 'data' caso contrario si queremos convertir una instancia a un diccionario (deserializar) usaremos el parametro 'instance'
            resultado = GolosinaSerializer(instance=nuevaGolosinaCreada)

            return Response(data={
                'message': 'Golosina creada exitosamente',
                'content': resultado.data  # diccionario convertido de la instancia
            }, status=status.HTTP_201_CREATED)

        else:
            # si la data no es valida (is_valid()) entonces los errores se almacenaran en el diccionario errors
            return Response(data={
                'message': 'Error al crear la golosina',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)
