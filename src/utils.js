import jsowebtoken from "jsonwebtoken";
import { conexion } from "./instancias.js";

// Middleware manual
export const validarToken = async (req, res, next) => {
  // donde se manda las tokens
  const authorization = req.headers.authorization;

  if (!authorization) {
    return res.status(403).json({
      message: "Se necesita una token para realizar esta peticion",
    });
  }

  // token > Bearer xxxxx.yyyy.zzzzz
  // split En base al caracter que le pongamos buscara en el texto y cada vez que encuentre ese caracter los separara en un arreglo
  // const texto = 'Hola como estan, yo bien y tu?
  // text.split(' ') > ['Hola', 'como', esta,', 'yo', 'bien', 'y', 'tu']
  const token = authorization.split(" ")[1]; // ['Bearer', 'xxxxx.yyyy.zzzz']

  if (!token) {
    return res.status(403).json({
      message: 'Debe enviar la token en format "Bearer YOUR_TOKEN"',
    });
  }

  // Verifica si la token es valida, tiene tiempo de vida y su firma es correcta (nosotros la hemos creado), si falla lanzara un error
  try {
    const payload = jsowebtoken.verify(token, process.env.JWT_SECRET); // { usuarioId: '....' }
    const usuarioEncontrado = await conexion.usuario.findUniqueOrThrow({
      where: { id: payload.usuarioId },
    });

    // Ahora agregamos en el request la propiedad usuario en la cual guardaremos nuestro usuario de la bd
    req.usuario = usuarioEncontrado;

    // al llamar a la funcion next estamos indicando que podra continuar con el siguiente middleware o controlador final
    next();
  } catch (error) {
    return res.status(403).json({
      message: "Error al verificar la token",
      content: error.message,
    });
  }
};
