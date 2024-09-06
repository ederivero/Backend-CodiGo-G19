import { Router } from "express";
import { crearEquipo, listarEquipos } from "./controllers/equipo.controller.js";
import {
  registroUsuario,
  login,
  perfilUsuario,
} from "./controllers/usuario.controller.js";
import asyncHandler from "express-async-handler";
import { validarToken, validarAdmin } from "./utils.js";
export const rutas = Router();

rutas
  .route("/equipos")
  .post(
    asyncHandler(validarToken),
    asyncHandler(validarAdmin),
    asyncHandler(crearEquipo)
  )
  .get(asyncHandler(listarEquipos));

rutas.route("/registro").post(asyncHandler(registroUsuario));

rutas.route("/login").post(asyncHandler(login));

rutas
  .route("/perfil")
  .get(asyncHandler(validarToken), asyncHandler(perfilUsuario));
