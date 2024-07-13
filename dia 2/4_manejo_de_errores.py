# todos los valores ingresados por teclado SIEMPRE seran str
informacion = input('Por favor ingresa un numero: ')

try:
    # print(10/0)
    # se realiza la conversion de un tipo de dato a otro
    informacion_numeros = int(informacion)
    print(informacion_numeros + 10)
    print(informacion)
except TypeError:
    # solo cuando error sea de tipo TypeError ingresara aca
    print('Hubo un error!!!')
except ZeroDivisionError:
    print('No se puede dividir entre 0!')
except Exception as e:
    print(type(e))  # obtener que tipo de erro es en el except generico
    print('Ocurrio otro error!')
