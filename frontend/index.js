const nombreLibro = document.getElementById("libro-nombre");
const descripcionLibro = document.getElementById("libro-descripcion");
const habilitadoLibro = document.getElementById("libro-habilitado");
const crearLibro = document.getElementById("crear-libro");
const BASE_URL = "http://127.0.0.1:3000";

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
