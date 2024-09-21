import { LibroModel } from "../models/libro.model.js";
import { obtenerSocket } from "../socket.js";
import { crearLibroDto } from "./dtos/libro.dto.js";

export const crearLibro = async (req, res) => {
  const { error, value } = crearLibroDto.validate(req.body);

  if (error) {
    throw new Error(error.details);
  }

  const nuevoLibro = await LibroModel.create({ ...value });
  const socket = obtenerSocket();

  // Emitir un evento para que se pueda escucharlo nuestro cliente
  socket.emit("libro_creado", { content: nuevoLibro.toJSON() });

  return res.status(201).json({
    message: "Libro creado exitosamente",
    content: nuevoLibro.toJSON(), // toJSON() > convierte el registro en un JSON legible
  });
};

export const listarLibros = async (req, res) => {
  const libros = await LibroModel.find();

  return res.json({
    content: libros,
  });
};

export const actualizarLibro = async (req, res) => {
  const { id } = req.params;

  const { error, value } = crearLibroDto.validate(req.body);

  if (error) {
    throw new Error(error.message);
  }

  const resultado = await LibroModel.findByIdAndUpdate(id, value, {
    // https://mongoosejs.com/docs/api/model.html#Model.findByIdAndUpdate()
    new: true, // devolver la informacion ya actualizada, sino devolvera la informacion previa a la actualizacion
  });

  const socket = obtenerSocket();

  socket.emit("libro_actualizado", { content: resultado.toJSON() });

  return res.json({
    message: "Libro actualizado exitosamente",
    content: resultado,
  });
};

export const eliminarLibro = async (req, res) => {
  const { id } = req.params;

  const resultado = await LibroModel.findByIdAndDelete(id);

  return res.json({
    message: "Libro eliminado exitosamente",
    content: resultado,
  });
};

// Crear un controlador para poder habilitar/deshabilitar el libro de manera automatica
// Solamente se mande el id
// 127.0.0.1:3000/a0s98da90s8d0a98sd
export const alternarHabilitado = async (req, res) => {
  const { id } = req.params;

  // Buscar si existe el libro
  const libroEncontrado = await LibroModel.findById(id);

  if (!libroEncontrado) {
    return res.status(404).json({
      message: "El libro no existe",
    });
  }
  // Si existe cambiar el valor de su 'habilitado'
  await LibroModel.updateOne(
    { _id: libroEncontrado._id },
    { habilitado: !libroEncontrado.habilitado }
  );

  // retornar un mensaje
  return res.json({
    message: "Libro modificado exitosamente",
  });
};
