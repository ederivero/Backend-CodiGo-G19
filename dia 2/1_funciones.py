numero = 10


# declaramos una funcion (definimos su comportamiento)
def incrementar_en_uno():
    print(1)


# llamamos a la ejecucion de la funcion
incrementar_en_uno()

# para llamar a la funcion se tiene que poner los parametros (que van entre parentesis) y si no llama a la funcion esta no se ejecutara, mas solo se obtendra su definicion
incrementar_en_uno


# si bien nosotros podemos declarar los tipos de datos que recibe una funcion en los parametros, estos no son de manera determinante, es decir al final podemos pasar cualquier tipo de dato diferente al declarado
def calcular_promedio(numero1: int, numero2: int):
    resultado = (numero1 + numero2) / 2
    # la funcion devolvera un valor
    return resultado


resultado_promedio = calcular_promedio(10, 40)

print(resultado_promedio)

nombre: str = 'Eduardo'


# Crear una funcion en la cual se pase un nombre y que se retorne el saludo 'Buenas noches NOMBRE'
def saludar(nombre):
    # EDUARDO > 'BUENAS NOCHES EDUARDO'
    saludo = 'Buenas noches '+nombre
    saludo = 'Buenas noches {}'.format(nombre)
    saludo = f'Buenas noches {nombre}'
    saludo = 'Buenas noches %s' % nombre

    return saludo


resultado = saludar('Eduardo')
print(resultado)


# Funciones que pueden recibir n parametros
# args > arguments
def numeros(*args):
    # Los argumentos ilimitados en el parametro son almacenados en una tupla, y esta recordemos que no se puede editar
    # los args generalmente sirven para almacenar una cantidad ilimitada de valores
    print(args)


numeros(10, 20, 40, 'a', True, 90.2, -10)


# kwargs > key arguments | Argumentos con llaves
def informacion(**kwargs):
    # el parametro kwargs se guardara en un dict cuyos parametros seran las llaves y cuyo valor seran los valores de las llaves
    print(kwargs)


informacion(nombre='Eduardo', casado=True,
            promedio=19.3, direccion='Calle los Florindios 1050')


# si queremos usar los args y los kwargs SIEMPRE primero van los args
def combinada(*args, **kwargs):
    print(args, kwargs)


combinada(10, 40, True, 0, 'etc', curso='Backend',
          nota='Es mejor que frontend')
