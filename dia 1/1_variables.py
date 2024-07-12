nombre = 'Eduardo'

edad = 32

soltero = True # Boolean > solamente o es True o es False

sueldo = 870.35

# Tipos de Datos PRIMITIVOS


nombre = -1
# En python los tipos de variables pueden cambiar sin ninguna restriccion

# java | c# | c++ no se puede cambiar el tipo de dato una vez creado

# Cada tipo de dato de las variables tienen sus propiedades y metodos definidos

# Las variables siempre deben empezar con letras

texto1 = 'Hola yo me llamo'
texto2 = 'Eduardo'

resultado = texto1 + texto2

print(resultado)

alumno1, alumno2, alumno3 = 'Ignacio', 'Segundo', 'Abel'

print(alumno1)

# upper > convierte el contenido a MAYUSCULAS
# Para toda la info relacionada a las variables TEXTO:
# https://docs.python.org/3/library/string.html#module-string
print(alumno1.upper())

# https://docs.python.org/3/library/functions.html#int

# split > separar el texto en base al caracter de busqueda
resultado = texto1.split(" ")
print(resultado)