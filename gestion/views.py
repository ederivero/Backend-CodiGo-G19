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
from .models import Usuario
from .serializers import RegistroSerializer


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

    return Response(data={
        'message': ''
    })
