import { Router } from "express";
import { crearEquipo, listarEquipos } from "./controllers/equipo.controller.js";
import asyncHandler from "express-async-handler";

export const rutas = Router();

rutas
  .route("/equipos")
  .post(asyncHandler(crearEquipo))
  .get(asyncHandler(listarEquipos));
