import AWS from "aws-sdk";
import { ImagenSerializer } from "../serializers/imagen.serializer.js";

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
    Key: `${path ? `/${path}` : ""}${key}.${extension}`, // Nombre con el cual se guarda el archivo en los servidores de S3
    Expires: 60, // Tiempo que durara el link disponible en segundos
    ContentType: contentType, // Sirve para indicar a aws que archivo puede subir MIME Type
  });

  return res.json({
    content: url,
  });
};
