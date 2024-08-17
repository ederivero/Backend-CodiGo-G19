from rest_framework.serializers import ModelSerializer
from .models import Categoria, Golosina


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        # especificar que atributos(columnas) vamos a utilizar para hacer la de/serializacion
        # fields = ['id', 'nombre']
        # si queremos utilizar todos los atributos del modelo (tabla)
        fields = '__all__'
        # si queremos utilizar la mayoria de los atributos pero obviar unos cuantos
        # exclude = ['id']

        # NOTA: no se puede utilizar el fields y el exclude al mismo tiempo, es uno o el otro


class GolosinaSerializer(ModelSerializer):
    class Meta:
        model = Golosina
        fields = '__all__'
