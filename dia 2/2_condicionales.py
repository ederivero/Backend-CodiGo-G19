numero1 = 45
numero2 = 50
numero3 = 40

# condicionales se pueden dar con resultado boolean
if numero1 > numero2:
    print('El numero 1 es mayor que el numero 2')

# si no cumple la primera condicion entonces trataremos con esta nueva y si no cumple entonces continuara al else o a otro elif si hubiese
elif numero1 > numero3:
    print('El numero 1 es mayor que el numero 3')

else:
    print('El numero 2 es mayor que el numero 1')


# Si tengo el sueldo entre 500 y 800 soles entonces puedo ir a la playa
# si tengo mas de 800 soles puedo ir al inti raymi
def calcular_actividades_vacacionales(sueldo: int):
    if sueldo >= 500 and sueldo <= 800:
        print('Sale playaso')
    elif sueldo > 800:
        print('Sale inti raymi')


sueldo = 600
# playaso
calcular_actividades_vacacionales(sueldo)

sueldo = 1300
# inti raymi
calcular_actividades_vacacionales(sueldo)


# Queremos saber si un alumno esta reprobado o necesita ir a vacacional o esta reprobado
# las condiciones son: si tiene entre 13 y 18 esta aprobado, si tiene entre 19 y 20 esta aprobado con felicitaciones, si tiene entre 11 y 12 necesita ir a vacacional y si tiene menos de 11 entonces esta reprobado
# convierta esto en una funcion en la cual se pase la nota y el nombre del estudiante

nota = 18
nombre = 'Eduardo'


def calcular_resultado_nota(nota, nombre):
    # modificar para no recibir notas menores que 0
    if nota < 0:
        print('No puede haber notas negativas')
    elif nota <= 10:
        print('El alumno {} esta reprobado'.format(nombre))
    elif nota <= 12:
        print('El alumno {} ira a vacacional'.format(nombre))
    elif nota <= 18:
        print('El alumno {} esta aprobado'.format(nombre))
    elif nota <= 20:
        print('El alumno {} esta aprobado con felicitaciones'.format(nombre))
    else:
        print('El alumno {} se va a la nasa con Wisin y Yandel'.format(nombre))


calcular_resultado_nota(-5, 'Eduardo')
