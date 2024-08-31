import { prisma } from "../cliente.js";
import { RecetaSerializer } from "../serializers/receta.serializer.js";

export async function crearReceta(req, res) {
  // Body del request
  const body = req.body; // {nombre: 'Tres leches de vainilla' }
  const resultado = await prisma.receta.create({
    data: {
      nombre: body.nombre,
      descripcion: body.descripcion,
    },
  });

  return res.json({
    message: "Receta creada exitosamente",
    content: resultado,
  });
}

export const listarRecetas = async (req, res) => {
  const resultado = await prisma.receta.findMany();

  return res.json({
    content: resultado,
  });
};

export const actualizarReceta = async (req, res) => {
  const body = req.body;
  // /receta/:id
  //  const id = req.params.id; // 125
  const { id } = req.params; // { id: 125 }

  const { error, value } = RecetaSerializer.validate(body);

  if (error) {
    return res.status(400).json({
      message: "Error al actualizar la receta",
      content: error.details,
    });
  }

  // SELECT id FROM receta WHERE id = '...';
  const recetaEncontrada = await prisma.receta.findUniqueOrThrow({
    // where: { id: parseInt(id) }, // { id:id }
    // Si tratamos de convertir un string invalido a un entero no lanzara error pero colocara el valor NaN (not a number)
    where: { id: +id },
    select: { id: true },
  });

  const recetaActualizada = await prisma.receta.update({
    where: { id: recetaEncontrada.id },
    data: {
      nombre: value.nombre,
      descripcion: value.descripcion,
      habilitado: value.habilitado,
    },
  });

  return res.json({
    message: "Receta actualizada exitosamente",
    content: recetaActualizada,
  });
};

export const eliminarReceta = async (req, res) => {
  const { id } = req.params;

  const recetaEncontrada = await prisma.receta.findUniqueOrThrow({
    where: { id: +id },
    select: { id: true },
  });

  const resultado = await prisma.receta.delete({
    where: { id: recetaEncontrada.id },
  });

  return res.json({
    message: "Receta eliminada exitosamente",
    content: resultado,
  });
};

export const listRecetaPorId = async (req, res) => {
  const { id } = req.params;

  const recetaEncontrada = await prisma.receta.findFirstOrThrow({
    where: { id: +id },
    // Incluir modelos anidados
    include: {
      ingredientes: true,
      preparaciones: {
        orderBy: { orden: "asc" },
      },
    },
  });

  return res.json({ content: recetaEncontrada });
};
