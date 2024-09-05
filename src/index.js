import express from "express";
import morgan from "morgan";
import { rutas } from "./router.js";

const servidor = express();

// Agregamos logger de los request de nuestro servidor
servidor.use(morgan("common"));

const PORT = process.env.PORT;
servidor.use(express.json());
servidor.use(rutas);

servidor.listen(PORT, () => {
  console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`);
});
