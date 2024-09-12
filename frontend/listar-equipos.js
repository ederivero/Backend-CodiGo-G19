const tabla = document.getElementById("equipos-table");
const BACKEND_URL = "http://127.0.0.1:3000";

const obtenerImagen = async (equipoId) => {
  const resultado = await fetch(`${BACKEND_URL}/imagen/equipo/${equipoId}`, {
    method: "GET",
  });

  return resultado.json();
};

const poblarTabla = async (data) => {
  for (const registro of data) {
    const fila = document.createElement("tr");
    const columnaNombre = document.createElement("td");
    const columnaImagen = document.createElement("td");

    const { content } = await obtenerImagen(registro.id);
    console.log(content);
    columnaImagen.innerHTML = `<img src=${content} height="100px"/>`;
    columnaNombre.innerText = registro.nombre;

    fila.appendChild(columnaNombre);
    fila.appendChild(columnaImagen);

    tabla.appendChild(fila);
  }
};

fetch(`${BACKEND_URL}/equipos`, { method: "GET" })
  .then((resultado) => {
    return resultado.json();
  })
  .then((data) => {
    // Aqui recibimos la informacion de los equipos
    console.log(data);
    poblarTabla(data.content);
  })
  .catch((e) => {
    console.error(e);
  });
