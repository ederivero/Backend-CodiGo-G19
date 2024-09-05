import { USUARIO_ROL } from "@prisma/client";
import Joi from "joi";

export const RegistroUsuarioSerializer = Joi.object({
  email: Joi.string().required().email(),
  password: Joi.string().required().regex(),
  rol: Joi.string()
    .required()
    .allow(USUARIO_ROL.ADMINISTRADOR, USUARIO_ROL.CLIENTE),
});
