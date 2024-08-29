import express from 'express'

const servidor = express()

// Le estamos indicando q nuestro servidor que pueda entender y convertir la informacion proveniente del body de tipo application/json
servidor.use(express.json())

servidor.get('/',(req, res) => {
    res.status(201).json({
        message:'Bienvenido a mi API de express'
    })
})

servidor.post('/registro', (req,res)=>{
    // Express tenemos que indicar que body va a poder recepcionar
    // Si va a recepcionar json | xml | txt | otros
    console.log(req.body)

    res.json({
        message:'Registro completado exitosamente'
    })
})

servidor.listen(3000, () => {
    console.log('Servidor de express levantado exitosamente')
})