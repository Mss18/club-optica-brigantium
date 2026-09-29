// JavaScript común de la aplicación.
// Validación de formularios con la API de HTML5 y estilos de Bootstrap.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form.needs-validation").forEach((form) => {
    form.addEventListener("submit", (evento) => {
      if (!form.checkValidity()) {
        evento.preventDefault();
        evento.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });
});
