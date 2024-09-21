import express from "express";
import { enrutador } from "./router.js";
import mongoose from "mongoose";
import cors from "cors";
import { createServer } from "http";
import { iniciarSocket } from "./socket.js";

const servidor = express();
// Agregamos toda la funcionabilidad de express en nuestro servidor http
const servidorHttp = createServer(servidor);

servidor.use(cors({ origin: "*" }));
servidor.use(express.json());

servidor.use(enrutador);

const errorHandler = (error, req, res, next) => {
  res.status(400).json({
    message: "Error al realizar la operacion",
    content: error.message,
  });
};

servidor.use(errorHandler);

servidorHttp.listen(process.env.PORT, async () => {
  await mongoose.connect(process.env.MONGODB_URL); // mongodb://USUARIO:PASSWORD@HOST:PORT/DB

  // Inicializamos nuestro servidor de los sockets para poder utilizarlo en toda la aplicacion
  iniciarSocket(servidorHttp);
  console.log(
    `Servidor corriendo exitosamente en el puerto ${process.env.PORT}`
  );
});
