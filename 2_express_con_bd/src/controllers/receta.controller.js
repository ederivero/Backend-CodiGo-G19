import { prisma } from "../cliente.js";

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
