import { Router } from "express";
import { crearEquipo } from "./controllers/equipo.controller.js";
// Agregar libreria para esperar los errores sincronos de nuestros controladores

export const rutas = Router();

rutas.route("/equipos").post(crearEquipo);
