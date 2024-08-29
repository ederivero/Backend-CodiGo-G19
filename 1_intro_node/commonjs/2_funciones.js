function restar(numero1, numero2){
    return numero1 - numero2
}

// Funciones anonimas
// se almacena en una variable

const multiplicacion = (numero1, numero2) => {
    return numero1 * numero2
}

// en una funcion anonima si solamente voy a tener una linea de codigo y esa linea la voy a retornar

const division = (numero1, numero2) => numero1 / numero2

const saludo ='hola'

// Usamos commonJS la exportacion se realiza en forma de modulos

module.exports = {
    restar,
    multiplicacion,
    division: division,
    saludo: saludo
}