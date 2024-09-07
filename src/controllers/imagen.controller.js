import AWS from "aws-sdk";
import { ImagenSerializer } from "../serializers/imagen.serializer.js";
import { conexion } from "../instancias.js";

export const generarUrlFirmada = async (req, res) => {
  const { error, value } = ImagenSerializer.validate(req.body);
  if (error) {
    return res.status(400).json({
      message: "Error al generar la imagen",
      content: error.details,
    });
  }

  const { key, path, contentType, extension } = value;

  const s3 = new AWS.S3();
  // getObject > obtener un archivo del s3
  // putObject > generar una url para subir un archivo al S3
  // deleteObject > eliminar un archivo del S3
  const url = s3.getSignedUrl("putObject", {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: `${path ? `${path}/` : ""}${key}.${extension}`, // Nombre con el cual se guarda el archivo en los servidores de S3
    Expires: 60, // Tiempo que durara el link disponible en segundos
    ContentType: contentType, // Sirve para indicar a aws que archivo puede subir MIME Type
  });

  return res.json({
    content: url,
  });
};

export const crearImagen = async (req, res) => {
  const { error, value } = ImagenSerializer.validate(req.body);

  if (error) {
    return res.status(400).json({
      message: "Error al crear la imagen",
      content: error.details,
    });
  }

  const imagenCreada = await conexion.imagen.create({ data: { ...value } });

  return res.status(201).json({
    content: imagenCreada,
    message: "Imagen creada exitosamente",
  });
};

export const devolverImagen = async (req, res) => {
  // http://127.0.0.1:3000/imagen/123123123-12312312-312313123
  const { id } = req.params;

  const imagenEncontrada = await conexion.imagen.findUniqueOrThrow({
    where: { id },
  });

  const s3 = new AWS.S3();

  const url = s3.getSignedUrl("getObject", {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: `${imagenEncontrada.path ? `${imagenEncontrada.path}/` : ""}${
      imagenEncontrada.key
    }.${imagenEncontrada.extension}`,
    Expires: 100,
  });

  return res.json({ content: url });
};
