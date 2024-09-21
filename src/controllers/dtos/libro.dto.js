import Joi from "joi";

export const crearLibroDto = Joi.object({
  nombre: Joi.string().optional(),
  descripcion: Joi.string().required(),
  habilitado: Joi.boolean().default(true),
});
