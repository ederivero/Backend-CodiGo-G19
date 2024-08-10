const pwd1 = document.getElementById('pwd1')
const pwd2 = document.getElementById('pwd2')
const confirm = document.getElementById('confirm-button')
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
    console.log(valor)
}).catch((error)=>{
    console.log('Hubo un error')
})