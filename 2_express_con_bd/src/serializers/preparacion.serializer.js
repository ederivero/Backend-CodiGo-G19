import Joi from "joi";

export const PreparacionSerializer = Joi.object({
  descripcion: Joi.string().required(),
  recetaId: Joi.number().required(),
});
