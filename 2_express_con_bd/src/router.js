import { Router } from "express";
import {
  crearReceta,
  listarRecetas,
  actualizarReceta,
  eliminarReceta,
  listRecetaPorId,
} from "./controllers/receta.controller.js";
import { crearIngrediente } from "./controllers/ingrediente.controller.js";
import { crearPreparacion } from "./controllers/preparacion.controller.js";
import asyncHandler from "express-async-handler";

export const enrutador = Router();

// Cuando utilizamos el mismo endpoint para dos o mas controladores se recomienda agruparlos
// enrutador.post("/recetas", crearReceta);
// enrutador.get("/recetas", listarRecetas);
enrutador
  .route("/recetas")
  .post(asyncHandler(crearReceta))
  .get(asyncHandler(listarRecetas));
enrutador
  .route("/receta/:id")
  .put(asyncHandler(actualizarReceta))
  .delete(asyncHandler(eliminarReceta))
  .get(asyncHandler(listRecetaPorId));

enrutador.route("/ingredientes").post(asyncHandler(crearIngrediente));

enrutador.route("/preparaciones").post(asyncHandler(crearPreparacion));
