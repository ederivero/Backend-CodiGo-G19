import prisma, { USUARIO_ROL } from "@prisma/client";
import bcrypt from "bcrypt";

const conexion = new prisma.PrismaClient();

async function alimentarBD() {
  const usuarios = [
    {
      nombre: "Renzo Soles Contreras",
      email: "rsoles@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.ADMINISTRADOR,
    },
    {
      nombre: "Abel Guevara",
      email: "aguevara@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.CLIENTE,
    },
    {
      nombre: "Rodrigo Trujillo Mirano",
      email: "rtrujillo@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.ADMINISTRADOR,
    },
    {
      nombre: "Segundo Alvarez",
      email: "salvarez@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.CLIENTE,
    },
    {
      nombre: "Ignacio Estremadoyro",
      email: "iestremadoyry@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.CLIENTE,
    },
  ];
  // Si tenemos un arreglo de promesas y queremos que todas finalicen exitosamente entonces la forma de esperarlas es con un Promise.all. si alguna falla entonces todas quedan sin efecto. retornara una Promesa
  await Promise.all(
    usuarios.map(async (usuario) => {
      // upsert > buscara el usuario en la bd, si lo encuentra actualizara su informacion, caso contrario lo creara
      await conexion.usuario.upsert({
        create: {
          email: usuario.email,
          rol: usuario.rol,
          password: usuario.password,
        },
        update: {
          // Para este escenario no actualizaremos nada
        },
        where: {
          email: usuario.email,
        },
      });
    })
  );
}

alimentarBD()
  .then(() => {
    console.log("Alimentacion a la base datos finalizada exitosamente");
  })
  .catch(() => {
    console.log("Error al alimentar la base de datos");
  });
