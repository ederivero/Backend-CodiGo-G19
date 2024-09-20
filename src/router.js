import express from "express";
import {
  crearLibro,
  listarLibros,
  actualizarLibro,
  eliminarLibro,
  alternarHabilitado,
} from "./controllers/libro.controller.js";
import asynHandler from "express-async-handler";

export const enrutador = express.Router();

enrutador
  .route("/libros")
  .post(asynHandler(crearLibro))
  .get(asynHandler(listarLibros));

enrutador
  .route("/libro/:id")
  .put(asynHandler(actualizarLibro))
  .delete(asynHandler(eliminarLibro));

enrutador.put("/alternar-libro/:id", asynHandler(alternarHabilitado));
