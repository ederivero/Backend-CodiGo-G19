import mongoose from "mongoose";

// Tablas > Collections
// Row    > Documents

const libroSchema = new mongoose.Schema(
  {
    // https://mongoosejs.com/docs/schematypes.html#all-schema-types
    nombre: mongoose.Schema.Types.String,
    habilitado: {
      type: mongoose.Schema.Types.Boolean,
      required: true, // al momento de crear si o si se tiene que pasar un valor a esta columna
      default: true,
    },
    descripcion: {
      type: mongoose.Schema.Types.String,
      maxLength: 200,
      trim: true, // Removera los espacios al comienzo y al final del texto
    },
  },
  {
    // https://mongoosejs.com/docs/guide.html#options
    timestamps: {
      updatedAt: "fecha_actualizacion",
      createdAt: true,
    },
  }
);

// Donde se creara la coleccion en la base de datos
export const LibroModel = mongoose.model("libros", libroSchema);
