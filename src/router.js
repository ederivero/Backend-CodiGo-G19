import { Router } from "express";
import { crearEquipo, listarEquipos } from "./controllers/equipo.controller.js";
import { registroUsuario, login } from "./controllers/usuario.controller.js";
import asyncHandler from "express-async-handler";

export const rutas = Router();

rutas
  .route("/equipos")
  .post(asyncHandler(crearEquipo))
  .get(asyncHandler(listarEquipos));

rutas.route("/registro").post(asyncHandler(registroUsuario));

rutas.route("/login").post(asyncHandler(login));
