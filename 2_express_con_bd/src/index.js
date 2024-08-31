import express from "express";
import { config } from "dotenv";
import { enrutador } from "./router.js";
// Lee el archivo .env y las configura como variables de entorno
config();

const servidor = express();

// Puedan entender la informacion proveniente del body en formato json
servidor.use(express.json());

const PUERTO = process.env.PORT;

// Un middleware -> intermediario en el cual se va gestionar los errores emitidos por prima o por otros factores
const errorHandler = (error, req, res, next) => {
  console.log(error);
  let mensajePersonalizado;
  let status;

  switch (error.message) {
    case "No Receta found":
      mensajePersonalizado = "La receta no existe";
      status = 404;
      break;

    case "No Preparacion found":
      mensajePersonalizado = "La preparacion no existe";
      status = 404;
      break;

    case "No Ingrediente found":
      mensajePersonalizado = "El ingrediente no existe";
      status = 404;
      break;

    default:
      mensajePersonalizado = error.message;
      status = 400;
  }

  res.status(status).json({
    message: "Error al hacer la operacion",
    content: mensajePersonalizado,
  });
};

// Estamos agregando todas las rutas de nuestro enrutador a nuestro proyecto de express
servidor.use(enrutador);

// Ahora agregamos la funcion como middleware
// Una vez que el error ha sido emitido en el controlador lo vamos a recibir en el middleware antes de retornar la informacion al usuario
servidor.use(errorHandler);

servidor.listen(PUERTO, () => {
  console.log(`Servidor corriendo exitosamente en el puerto ${PUERTO}`);
});
