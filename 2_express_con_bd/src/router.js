import { Router } from "express";
import { crearReceta } from "./controllers/receta.controller.js";

export const enrutador = Router();

enrutador.post("/recetas", crearReceta);
