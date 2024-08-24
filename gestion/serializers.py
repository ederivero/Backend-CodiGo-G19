from rest_framework import serializers
from .models import Usuario, ListaNovio

# ModelSerializer > Sirve para crear un serializador PERO basandonos en un modelo de nuestros Models, es decir, utilizara todos los atributos (Columnas) del modelo para hacer las validaciones (not null, unique, primary key, etc)
# Serializer > Crear un serializador pero sin la necesidad de basarse en un model (tabla) sino que completamente modificable y no tendra como base un modelo (tabla)


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        # fields = '__all__'
        exclude = ['password', 'is_staff', 'is_superuser',
                   'is_active', 'groups', 'user_permissions']
        # sirve para agregar configuracion adicional a los atributos de la clase
        extra_kwargs = {
            # write_only > sea utilizado cuando se quiera agregar un valor a la bd (escritura)
            # read_only > sea utilizado cuando se quiera LEER el valor y devolverlo de la bd (lectura)
            'last_login': {'write_only': True}
        }


class NovioSerializer(serializers.Serializer):
    # https://www.django-rest-framework.org/api-guide/fields/
    nombre = serializers.CharField(required=True)
    apellido = serializers.CharField(required=True)
    correo = serializers.EmailField(required=True)
    numeroTelefonico = serializers.CharField(required=True)
    password = serializers.CharField()


class ListaNoviosCreacionSerializer(serializers.Serializer):
    novio = NovioSerializer(required=True)
    novia = NovioSerializer(required=True)


class ListaNovioSerializer(serializers.ModelSerializer):
    # Si queremos definir atributos a mostrar (no todos) de los modelos anidados
    novio = UsuarioSerializer()
    # si queremos cambiar el nombre del atributo por otro y para seguir utilizando el valor del atributo antiguo tenemos que utilizar el parametro source e indicar que atributo usaremos para crear en el serializador el nuevo atributo. No se puede colocar el mismo nombre y el source
    laNovia = UsuarioSerializer(source='novia')
    # novia = UsuarioSerializer(source='novia')

    class Meta:
        model = ListaNovio
        fields = '__all__'
        # si en nuestro modelo actual tenemos llaves foraneas (FK) podemos acceder a su informacion adyacente mediante la profundidad, en base al numero que pongamos ingresaremos a cuantos vecinos tengamos
        # lista_novios(novio_id) > novios(ciudad_id) > ciudades(pais_id) paises
        # depth = 1
        # ingresara la lista novios y a los novios
        # depth = 2
        # ingresara la lista novios, a los novios y a las ciudades
        # depth = 3
        # ingresara la lista novios, a los novios, a las ciudades y al pais
        # depth = 1
