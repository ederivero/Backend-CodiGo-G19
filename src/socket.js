import { Server } from "socket.io";

let servidorSocket;

export const iniciarSocket = (servidorHttp) => {
  servidorSocket = new Server(servidorHttp, {
    cors: {
      origin: "*", // ["https://mifrontend.com", "http://mipaginafraudulenta.com"],
    },
  });

  // on sirve para indicar un evento que esperaremos que empiece el cliente para la conexion
  servidorSocket.on("connection", (cliente) => {
    console.log(cliente.id);

    // Emitimos un evento al cliente que se ha conectado
    // Se va a emitir al cliente que se ha conectado
    cliente.emit("saludo", "Buenas noches");

    // Dispara el evento a todos los usuario conectados EXCEPTO al cliente
    cliente.broadcast.emit("informacion", {
      message: `El cliente ${cliente.id} se ha conectado`,
    });

    cliente.on("solicitar_hora_sistema", (argumentos) => {
      console.log(argumentos);
      // Tbn podemos emitir un evento a TOOOOODOS los clientes conectados
      servidorSocket.emit("evento_de_la_hora_del_sistema", {
        message: "ALGUIEN SOLICITO LA HORA",
      });
    });
  });
};

export const obtenerSocket = () => {
  if (!servidorSocket) {
    throw new Error("El servidor de los socket no ha sido inicializado");
  }

  return servidorSocket;
};
