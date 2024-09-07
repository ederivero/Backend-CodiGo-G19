const btnComenzar = document.getElementById("btnComenzar");
const nombreEquipo = document.getElementById("nombreEquipo");
const imagenEquipo = document.getElementById("imagenEquipo");
const btnCrearEquipo = document.getElementById("btnCrearEquipo");

btnComenzar?.addEventListener("click", (e) => {
  e.preventDefault();
  window.location.href = "crear-equipo.html";
});

console.log(window.location.pathname);

// Cuando estemos en crear Equipo

if (window.location.pathname.includes("crear-equipo.html")) {
  console.log("enntro");
}
