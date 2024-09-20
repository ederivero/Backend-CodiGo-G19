import express from "express";
import { enrutador } from "./router.js";
import mongoose from "mongoose";

const servidor = express();

servidor.use(express.json());

servidor.use(enrutador);

const errorHandler = (error, req, res, next) => {
  res.status(400).json({
    message: "Error al realizar la operacion",
    content: error.message,
  });
};

servidor.use(errorHandler);

servidor.listen(process.env.PORT, async () => {
  await mongoose.connect(process.env.MONGODB_URL); // mongodb://USUARIO:PASSWORD@HOST:PORT/DB
  console.log(
    `Servidor corriendo exitosamente en el puerto ${process.env.PORT}`
  );
});
