import Joi from "joi";

export const crearEquipoSerializer = Joi.object({
  nombre: Joi.string().required(),
  imagen: Joi.string().optional(),
});
