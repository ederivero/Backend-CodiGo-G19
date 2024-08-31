import { prisma } from "../cliente.js";
import { PreparacionSerializer } from "../serializers/preparacion.serializer.js";

export const crearPreparacion = async (req, res) => {
  const { error, value } = PreparacionSerializer.validate(req.body);

  if (error) {
    return res.status(400).json({
      message: "Error al crear la preparacion",
      content: error.details,
    });
  }

  // Buscar si ya existe una preparacion de la receta
  // SELECT orden FROM preparaciones WHERE receta_id = '...' ORDER BY orden DESC;
  const preparacionExistente = await prisma.preparacion.findFirst({
    where: { recetaId: value.recetaId },
    orderBy: { orden: "desc" }, // 3 > 2 > 1
    select: { orden: true },
  });

  //   let nuevaPosicion;
  //   // Si ya existe obtener la ultima preparacion
  //   if (preparacionExistente) {
  //     nuevaPosicion = preparacionExistente.orden + 1;
  //   } else {
  //     // Si no existe entonces crear con el orden numero 1
  //     nuevaPosicion = 1;
  //   }

  const nuevaPosicion = preparacionExistente
    ? preparacionExistente.orden + 1
    : 1;

  const nuevaPreparacion = await prisma.preparacion.create({
    data: {
      descripcion: value.descripcion,
      recetaId: value.recetaId,
      orden: nuevaPosicion,
    },
  });

  return res.status(201).json({
    message: "Preparacion creada existosamente",
    content: nuevaPreparacion,
  });
};
