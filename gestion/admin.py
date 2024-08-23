from django.contrib import admin
from .models import Usuario

# Si queremos hacer alguna configuracion adicional a los modelos, entonces usaremos una clase


class UsuarioAdmin(admin.ModelAdmin):
    # Mensaje en el caso que en una columna no exista valor (null)
    empty_value_display = 'NO HAY'

    # Como queremos mostrar los registros de nuestro modelo
    list_display = ['nombre', 'apellido', 'correo']

    # Lista de atributos en la cuales queremos excluir para ya sea crear o actualizar nuestro registro
    exclude = ['nombre']

    # indicar en que columnas yo puedo seleccionar al usuario para ver su informacion o editaro
    list_display_links = ['nombre', 'apellido']

    # sirve para poder agregar un filtrado en nuestro modelo y esto servira para una busqueda mas rapida
    list_filter = ['nombre', 'apellido']

    # hacer busquedas usando llaves foraneas o relaciones de muchos a muchos
    # autocomplete_fields = ['nombre']

    # Agrega un buscador y se le coloca los atributos que tiene que buscar, no es sensible a mayus o minus
    search_fields = ['nombre', 'apellido']


admin.site.register(Usuario, UsuarioAdmin)
