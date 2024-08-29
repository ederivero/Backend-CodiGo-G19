import {restar} from './2_funciones.mjs'
// Si una variable va a cambiar su valor mas de una vez entonces no se usa const sino se usa let
let x = 'eduardo'

x = 'ramiro'
x = 'Juan'
x = 20
console.log('Hola')

function sumar(numero1, numero2) {
    const resultado = numero1 + numero2

    return resultado
}

const sumatoria = sumar(10,20)

console.log(sumatoria)

const resta = restar(50,30)
console.log(resta)