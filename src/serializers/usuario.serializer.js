import { USUARIO_ROL } from "@prisma/client";
import Joi from "joi";

export const RegistroUsuarioSerializer = Joi.object({
  email: Joi.string().required().email(),
  password: Joi.string()
    .required()
    // [a-z] > Al menos una minuscula
    // [A-Z] > Al menos una mayuscula
    // *d > Al menos un digito
    // [W_] > Al menos un caracter especial
    // {6,} > Longitud minima de 6 caracteres
    .regex(new RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[W_]).{6,}$/)),
  rol: Joi.string()
    .required()
    .allow(USUARIO_ROL.ADMINISTRADOR, USUARIO_ROL.CLIENTE),
});

export const LoginSerializer = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required(),
});
