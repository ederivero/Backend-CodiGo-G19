texto = 'Hola a todos" como estan'

texto2 = "Hola a todos' como estan"

# Bloque de texto
texto_largo = """y juanita exclamo: Ojala mañana sea viernes 
  A lo que Pedrito dijo: Pero si mañana ya es viernes!
Y Ramon adiciono: Hay festival de carnes y cerveza! """

texto_largo_2 = '''y juanita exclamo: Ojala mañana sea viernes 
A lo que Pedrito dijo: Pero si mañana ya es viernes!'''



print(texto_largo)
print(texto[1])

# Imprima la ultima letra del texto
print(texto[-1])

# Extraer una sub cadena mi texto
print(texto[1:6])

# Desde el comienzo (posicion 0) hasta la posicion 10
print(texto[:10])

# Desde la posicion 20 hasta el final
print(texto[20:])

# No importa si el inicio es + o - siempre el recorrido sera hacia la derecha
print(texto[-2:])

# Tener cuidad al momento de poner limites ya que si le ponemos un limite incorrecto no lanzara error pero devolvera informacion incorrecta
print(texto[4:2])