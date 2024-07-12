# Coleccion de datos es una variable que puede guardar varios valores 

# Listas (List) (arreglo)
frutas = ['manzana', "platano", 'papaya', "granadilla", 'papaya']
# Ordenada (tienen un indice de busqueda)
# Editable (se puede agregar y quitar elementos)
print(frutas[0])

# agregar nuevos valores
frutas.append('uva')
print(frutas)

# elimina el valor de la lista segun su indice ademas retorna el valor
fruta_eliminada = frutas.pop(0)
# si queremos eliminar un elemento pero por su valor usamos el metodo remove
# si tenemos dos o mas veces el valor repetido solo eliminara la primera concordancia
# si no existe ningun elemento con ese valor lanzara un error
frutas.remove('papaya')

# cuando nosotros colocamos el indice y le asignamos un valor, este reemplazara el valor actual
frutas[0] = 'palta'

# no se puede utilizar un indice que no existe para reemplazar un elemento
# frutas[7] = 'fresa'
print(fruta_eliminada)
print(frutas)

# len > longitud ya sea de textos, listas, tuplas, set
texto = 'hola soy su profe'
print(len(frutas))
print(len(texto))

# tuplas
# Es ordenada
# No se puede editar (ineditable)
meses = ('Enero', 'Febrero', 'Marzo')

# Mantener el mismo contenido durante toda la ejecucion del archivo o programa
# Aca se suele guardar informacion que no va a cambiar en toda la ejecucion del programa
print(meses[1])


# sets
# Es desornedada 
# si es editable
alumnos = {
    'Abel',
    'Cristhian',
    'Denys',
    'Andree',
    'Giancarlo',
    'Ignacio',
    'Luis',
    'Segundo',
    'Rodrigo',
    'Renzo'
}

# sirve para ver si esta o no esta
print('Denys' in alumnos)
print('Eduardo' in alumnos)

# agregar elementos a un set
alumnos.add('Arnold')
alumnos.remove('Luis')
print(alumnos)


# Dict - Diccionario
# es ordenado PEEEERO no utiliza indices sino que usa LLAVES (KEYS)
persona = {
    'nombre': 'Eduardo',
    'nombre': 'Juanito',
    'apellido': 'de Rivero',
    'sexo': 'Masculino',
    'hobbies': ['Comer', 'Programar', 'Montar bici'],
    'direccion': {
        'calle': 'calle las paltas',
        'numero': 1050,
        'zip_code': '04018'
    },
    'casado': False,
    'estatura': 1.60
}

# Si utilizamos una KEY que no exista, creara esa nueva key caso contrario reemplazara el valor antiguo
persona['edad'] = 32
persona['estatura'] = 1.65

print(persona)

# Como puedo obtener el nombre de la persona
print(persona['nombre'])

# como puedo obtener cuantos hobbies tiene la persona
print(len(persona['hobbies']))

# como puedo obtener el zip_code de la direccion de la persona
print(persona['direccion']['zip_code'])
