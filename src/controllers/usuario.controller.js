import {
  RegistroUsuarioSerializer,
  LoginSerializer,
} from "../serializers/usuario.serializer.js";
import bcrypt from "bcrypt";
import { conexion } from "../instancias.js";
import jsonwebtoken from "jsonwebtoken";

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
    select: { email: true, id: true, rol: true },
  });

  return res.status(201).json({
    message: "Usuario creado exitosamente",
    content: usuarioCreado,
  });
};

export const login = async (req, res) => {
  const { error, value } = LoginSerializer.validate(req.body);

  if (error) {
    return res.status(400).json({
      message: "Error al hacer el login",
      content: error.details,
    });
  }

  const usuarioEncontrado = await conexion.usuario.findUniqueOrThrow({
    where: { email: value.email },
  });

  const esLaPassword = bcrypt.compareSync(
    value.password,
    usuarioEncontrado.password
  );

  if (esLaPassword === false) {
    // No es la password
    return res.status(400).json({
      message: "La password es incorrecta",
    });
  }

  // Generamos la JWT
  const token = jsonwebtoken.sign(
    { usuarioId: usuarioEncontrado.id },
    process.env.JWT_SECRET,
    // Si colocamos numeros entonces el valor sera representado en milisegundos
    // Caso contrario utilizaremos el formato
    // 2 days | 2d
    // 10 hours | 10h
    // 5 seconds | 5s
    // 1 year | 1y
    { expiresIn: "5h" }
  );

  return res.json({
    content: token,
  });
};

export const perfilUsuario = async (req, res) => {
  return res.json({
    message: "El perfil es",
  });
};
