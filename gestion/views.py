from django.db.models import Q
from datetime import datetime
from os import environ
from cloudinary import utils
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    # Permite que cualquier usuario tenga o no de la token de acceso pueda acceder al endpoint
    AllowAny,
    # Validara que en la peticion se de una token valida y que tenga tiempo de vida
    IsAuthenticated,
    # A parte de la validacion solamente pasara si el usuario es ADMIN (is_superuser = True)
    IsAdminUser,
    # Si el metodo a acceder es GET no sera necesaria la token, caso contrario sera obligatoria (x ejemplo para un post , put, delete)
    IsAuthenticatedOrReadOnly
)
from .models import Usuario, ListaNovio, Regalo
from .serializers import RegistroSerializer, UsuarioSerializer, ListaNoviosCreacionSerializer, ListaNovioSerializer, RegaloSerializer
from .permissions import EsAdministrador, EsNovio
from django.db import transaction


@api_view(http_method_names=['POST'])
def crearUsuario(request):
    body = request.data
    # cuando queremos validar la informacion proveniente del body usamos el parametro data
    # cuando queremos convertir la informacion proveniente de la bd usamos el parametros instance
    serializador = RegistroSerializer(data=body)

    if serializador.is_valid():
        nuevo_usuario = Usuario(nombre=serializador.validated_data['nombre'],
                                apellido=serializador.validated_data['apellido'],
                                correo=serializador.validated_data['correo'],
                                numeroTelefonico=serializador.validated_data['numeroTelefonico'],
                                tipoUsuario=serializador.validated_data['tipoUsuario'])

        nuevo_usuario.set_password(serializador.validated_data['password'])

        # Solo si estamos utilizando el panel administrativo haremos la siguiente validacion
        if serializador.validated_data['tipoUsuario'] == 'ADMIN':
            nuevo_usuario.is_superuser = True

        nuevo_usuario.save()

        return Response(data={
            'message': 'Usuario creado exitosamente'
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(data={
            'message': 'Error al crear el usuario',
            # errors > mostrara todos los errores que el serializador me dara sobre porque la data no es valida
            'content': serializador.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
# agregar ciertos permisos a una api_view entonces usaremos permission_classes
@permission_classes([IsAuthenticated])
def perfilUsuario(request):

    print(request.user.nombre)
    print(request.auth)
    # cuando queremos pasar una instancia a nuestro serializador usaremos el parametro instance, sin embargo si queremos pasarle informacion para que la valide usaremos el parametro data
    serializador = UsuarioSerializer(instance=request.user)

    return Response(data={
        'content': serializador.data
    })


class ListaNoviosAPIView(APIView):
    # Primero validara que el usuario este autenticado y luego validara que sea administrador
    permission_classes = [IsAuthenticated, EsAdministrador]

    def post(self, request):
        serializador = ListaNoviosCreacionSerializer(data=request.data)
        if serializador.is_valid():
            print(serializador.validated_data)
            # utilizar transacciones de sql
            # https://docs.djangoproject.com/en/5.1/topics/db/transactions/
            with transaction.atomic():
                # todo lo que hagamos tiene que completarse exitosamente, si algo falla entonces todas las inserciones, actualizaciones y eliminaciones quedaran sin efecto
                nuevoNovio = Usuario(nombre=serializador.validated_data.get('novio').get('nombre'),
                                     apellido=serializador.validated_data.get(
                                         'novio').get('apellido'),
                                     correo=serializador.validated_data.get(
                                         'novio').get('correo'),
                                     tipoUsuario='NOVIO',
                                     numeroTelefonico=serializador.validated_data.get('novio').get('numeroTelefonico'))

                nuevoNovio.set_password(
                    serializador.validated_data.get('novio').get('password'))

                nuevoNovia = Usuario(nombre=serializador.validated_data.get('novia').get('nombre'),
                                     apellido=serializador.validated_data.get(
                                         'novia').get('apellido'),
                                     correo=serializador.validated_data.get(
                                         'novia').get('correo'),
                                     numeroTelefonico=serializador.validated_data.get(
                                         'novia').get('numeroTelefonico'),
                                     tipoUsuario='NOVIO')

                nuevoNovia.set_password(
                    serializador.validated_data.get('novia').get('password'))

                nuevoNovio.save()
                nuevoNovia.save()

                nuevaLista = ListaNovio(
                    novio=nuevoNovio, novia=nuevoNovia)
                nuevaLista.save()

            print(nuevaLista)
            return Response(data={
                'message': 'Lista creada exitosamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message': 'Error al crear la lista de novios',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        resultado = ListaNovio.objects.all()
        # Si al parametro instance le vamos a pasar una lista entonces tenemos que indicarle al serializador para que pueda hacer la iteracion de la lista y transformar cada uno de los elementos
        serializador = ListaNovioSerializer(instance=resultado, many=True)

        return Response(data={
            'content': serializador.data
        })


class RegalosAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, EsNovio]

    def post(self, request):
        # TAREA!
        # Crear un serializador para obtener la informacion de crear un regalo
        # en el campo de la imagen enviar la url que cloudinary nos brinda (la segura)
        # Solamente LOS NOVIOS PUEDEN agregar regalos y buscar la lista de novios del novio o novia en la cual se quiere agregar el regalo
        print(request.user)
        # SELECT * FROM lista_novios WHERE novio_id = '...' OR novia_id = '...';
        listaEncontrada = ListaNovio.objects.filter(
            Q(novio=request.user) | Q(novia=request.user))

        print(listaEncontrada)
        serializador = RegaloSerializer(data=request.data)
        if serializador.is_valid():

            return Response(data={
                'message': 'Regalo creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message': 'Hubo un error ',
                'content': serializador.errors
            })

    def get(self, request):
        # Retornar todos los regalos del novio que actualmente esta logeado

        # SELECT * FROM lista_novios WHERE novio_id = 1 LIMIT 1 ;
        listNovioEncontrado = ListaNovio.objects.filter(novio=1).first()
        regalos = Regalo.objects.filter(
            listaNovio=listNovioEncontrado.id).all()

        return Response(data={
            'message': ''
        })


@api_view(http_method_names=['POST'])
def generarCloudinaryUrl(request):
    timestamp = datetime.now().timestamp()
    signature = utils.api_sign_request(
        {'timestamp': timestamp}, environ.get('CLOUDINARY_API_SECRET'))

    url = f'https://api.cloudinary.com/v1_1/{environ.get('CLOUDINARY_NAME')}/image/upload?api_key={
        environ.get('CLOUDINARY_API_KEY')}&timestamp={timestamp}&signature={signature}'
    return Response({
        'content': url
    })
