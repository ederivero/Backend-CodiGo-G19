import express from "express";
import morgan from "morgan";

const servidor = express();

// Agregamos logger de los request de nuestro servidor
servidor.use(morgan("common"));

const PORT = process.env.PORT;

servidor.listen(PORT, () => {
  console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`);
});
