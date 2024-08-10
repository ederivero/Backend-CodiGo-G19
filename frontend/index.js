const pwd1 = document.getElementById('pwd1')
const pwd2 = document.getElementById('pwd2')
const cambiarPassword = document.getElementById('confirm-button')
const infoUsuario = document.getElementById('info-usuario')
const BACKEND_URL ='http://127.0.0.1:5000'

// Asi se leen los query params en el frontend
const queryString = window.location.search
console.log(queryString)
const urlParams = new URLSearchParams(queryString)
const token = urlParams.get('token')

fetch(`${BACKEND_URL}/validar-token`,{
    method:'POST', 
    body: JSON.stringify({token:token}),
    headers:{
        'Content-Type': 'application/json'
    }
}).then((valor)=> {
    return valor.json()
}).then((data)=> {
    console.log(data)
    infoUsuario.innerText = `Bienvenido ${data.content.nombre} ingresa dos veces tu nueva contraseña para hacer el cambio de la misma`
}).catch((error)=>{
    console.log('Hubo un error')
})


cambiarPassword.addEventListener('click',(event)=>{
    event.preventDefault()
    const valor1 = pwd1.value
    const valor2 = pwd2.value
    
    if(valor1 !== valor2) {
        alert('Las contraseñas no coinciden!')
    }
    else{
        const body = {
            token,
            nuevaPassword: valor1
        }
        fetch(`${BACKEND_URL}/confirm-reset-password`, {
            method: 'POST',
            body: JSON.stringify(body),
            headers:{
                'Content-Type': 'application/json'
            }
        }).then((value)=>{
            return value.json()
        }).then((data)=>{
            console.log(data)
        }).catch((error)=>{
            console.log(error)
        })
    }
})