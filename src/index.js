import express from "express";
import { enrutador } from "./router.js";
import mongoose from "mongoose";
import { Server } from "socket.io";
import { createServer } from "http";

const servidor = express();
// Agregamos toda la funcionabilidad de express en nuestro servidor http
const servidorHttp = createServer(servidor);
const servidorSocket = new Server(servidorHttp, {
  cors: {
    origin: "*", // ["https://mifrontend.com", "http://mipaginafraudulenta.com"],
  },
});

servidor.use(express.json());

servidor.use(enrutador);

const errorHandler = (error, req, res, next) => {
  res.status(400).json({
    message: "Error al realizar la operacion",
    content: error.message,
  });
};

// on sirve para indicar un evento que esperaremos que empiece el cliente para la conexion
servidorSocket.on("connection", (cliente) => {
  console.log(cliente.id);

  // Emitimos un evento al cliente que se ha conectado
  // Se va a emitir al cliente que se ha conectado
  cliente.emit("saludo", "Buenas noches");

  cliente.on("solicitar_hora_sistema", (argumentos) => {
    console.log(argumentos);
    // Tbn podemos emitir un evento a TOOOOODOS los clientes conectados
    servidorSocket.emit("evento_de_la_hora_del_sistema", {
      message: "ALGUIEN SOLICITO LA HORA",
    });
  });
});

servidor.use(errorHandler);

servidorHttp.listen(process.env.PORT, async () => {
  await mongoose.connect(process.env.MONGODB_URL); // mongodb://USUARIO:PASSWORD@HOST:PORT/DB
  console.log(
    `Servidor corriendo exitosamente en el puerto ${process.env.PORT}`
  );
});
