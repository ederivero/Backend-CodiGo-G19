import Joi from "joi";

export const IngredienteSerializer = Joi.object({
  titulo: Joi.string().required(),
  recetaId: Joi.number().required(),
});
