import express from "express";
import morgan from "morgan";
import { rutas } from "./router.js";

const servidor = express();

const errorHandler = (error, req, res, next) => {
  res.status(400).json({
    message: "Error al realizar la operacion",
    content: error.message,
  });
};

// Agregamos logger de los request de nuestro servidor
servidor.use(morgan("common"));

const PORT = process.env.PORT;
servidor.use(express.json());
servidor.use(rutas);
servidor.use(errorHandler);

servidor.listen(PORT, () => {
  console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`);
});
