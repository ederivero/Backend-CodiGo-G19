import Joi from "joi";

export const crearEquipoSerializer = Joi.object({
  nombre: Joi.string().required(),
  imagenId: Joi.string().optional(),
});
