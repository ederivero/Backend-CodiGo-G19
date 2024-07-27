def sumar(numero1, numero2):
    return numero1 + numero2

resultado  =sumar(10,5)

print(resultado)


datos = {
    'numero1': 20,
    'numero2': 40
}

resultado = sumar(datos['numero1'], datos['numero2'])
print(resultado)

resultado = sumar(numero1=datos['numero1'],numero2= datos['numero2'])
print(resultado)

resultado = sumar(**datos)
print(resultado)