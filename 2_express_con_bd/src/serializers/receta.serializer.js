import Joi from "joi";

export const RecetaSerializer = Joi.object({
  nombre: Joi.string().required(),
  descripcion: Joi.string().optional(),
  habilitado: Joi.boolean().optional().default(true),
});
