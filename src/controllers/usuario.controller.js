import { RegistroUsuarioSerializer } from "../serializers/usuario.serializer.js";
import bcrypt from "bcrypt";
import { conexion } from "../instancias.js";

export const registroUsuario = async (req, res) => {
  const { error, value } = RegistroUsuarioSerializer.validate(req.body);

  if (error) {
    return res.status(400).json({
      message: "Error al registrar el usuario",
      content: error.details,
    });
  }

  const passwordHashed = bcrypt.hashSync(value.password, 10);
  const usuarioCreado = await conexion.usuario.create({
    data: { email: value.email, password: passwordHashed, rol: value.rol },
  });

  return res.status(201).json({
    message: "Usuario creado exitosamente",
    content: usuarioCreado,
  });
};
