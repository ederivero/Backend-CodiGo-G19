import { IngredienteSerializer } from "../serializers/ingrediente.serializer.js";
import { prisma } from "../cliente.js";

export const crearIngrediente = async (req, res) => {
  const { error, value } = IngredienteSerializer.validate(req.body);

  if (error) {
    return res.status(400).json({
      message: "Error al crear el ingrediente",
      content: error.details,
    });
  }

  // Buscar la receta que exista
  const recetaEncontrada = await prisma.receta.findUniqueOrThrow({
    where: { id: value.recetaId },
    select: { id: true },
  });

  // Crear el ingrediente

  const ingredienteCreado = await prisma.ingrediente.create({
    data: {
      titulo: value.titulo,
      recetaId: recetaEncontrada.id,
    },
  });

  return res.status(201).json({
    message: "Ingrediente creado exitosamente",
    content: ingredienteCreado,
  });
};
