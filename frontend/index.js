const nombreLibro = document.getElementById("libro-nombre");
const descripcionLibro = document.getElementById("libro-descripcion");
const habilitadoLibro = document.getElementById("libro-habilitado");
const crearLibro = document.getElementById("crear-libro");
const listarLibros = document.getElementById("listar-libros");
const BASE_URL =
  "https://42c5-2001-1388-53a0-dff7-686e-4e84-a903-300c.ngrok-free.app";

const socket = io(BASE_URL);

crearLibro.addEventListener("click", (e) => {
  e.preventDefault();
  fetch(`${BASE_URL}/libros`, {
    method: "POST",
    body: JSON.stringify({
      nombre: nombreLibro.value,
      descripcion: descripcionLibro.value,
      habilitado: habilitadoLibro.checked,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((r) => r.json())
    .then((respuesta) => {
      console.log(respuesta);
    });
});

fetch(`${BASE_URL}/libros`, { method: "GET" })
  .then((r) => r.json())
  .then((respuesta) => {
    respuesta.content.forEach((libro) => {
      const div = document.createElement("div");
      div.id = libro._id;
      div.classList.add("card", "m-2");
      div.style.width = "18rem";

      const html = `
      <div class="card-body">
      <h5 class="card-title">${libro.nombre}</h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">${
        libro.descripcion
      }</h6>
      <p class="card-text">${
        libro.habilitado ? "Disponible" : "No Disponible"
      }</p>
        </div>`;

      div.innerHTML = html;
      listarLibros.appendChild(div);
    });
  });

socket.on("libro_creado", (informacion) => {
  const div = document.createElement("div");
  div.classList.add("card", "m-2");
  div.style.width = "18rem";
  div.id = informacion.content._id;

  const html = `
    <div class="card-body">
    <h5 class="card-title">${informacion.content.nombre}</h5>
    <h6 class="card-subtitle mb-2 text-body-secondary">${
      informacion.content.descripcion
    }</h6>
    <p class="card-text">${
      informacion.content.habilitado ? "Disponible" : "No Disponible"
    }</p>
      </div>`;

  div.innerHTML = html;
  listarLibros.appendChild(div);
});

// Recibir un evento desde el servidor
socket.on("libro_actualizado", (informacion) => {
  for (const child of listarLibros.childNodes) {
    if (informacion.content._id === child.id) {
      const html = `
    <div class="card-body">
    <h5 class="card-title">${informacion.content.nombre}</h5>
    <h6 class="card-subtitle mb-2 text-body-secondary">${
      informacion.content.descripcion
    }</h6>
    <p class="card-text">${
      informacion.content.habilitado ? "Disponible" : "No Disponible"
    }</p>
      </div>`;
      child.innerHTML = html;
    }
  }
});

// Emitir un evento desde el cliente
socket.emit("solicitar_hora_sistema", { data: "blablabla" });
