const form = document.getElementById("form-producto");
const tabla = document.getElementById("tabla-productos");
const mensaje = document.getElementById("mensaje");

function mostrarMensaje(texto, tipo) {
  mensaje.hidden = false;
  mensaje.textContent = texto;
  mensaje.className = `mensaje ${tipo}`;
}

function renderProductos(productos) {
  tabla.innerHTML = productos
    .map(
      (producto) => `
        <tr>
          <td>${producto.id}</td>
          <td>${producto.nombre}</td>
          <td>${producto.categoria}</td>
          <td>$${Number(producto.precio).toFixed(2)}</td>
        </tr>
      `
    )
    .join("");
}

async function cargarProductos() {
  const respuesta = await fetch("/api/productos");
  const productos = await respuesta.json();
  renderProductos(productos);
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(form);
  const cuerpo = {
    nombre: datos.get("nombre"),
    categoria: datos.get("categoria"),
    precio: datos.get("precio"),
  };

  const respuesta = await fetch("/api/productos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cuerpo),
  });

  const resultado = await respuesta.json();
  if (!respuesta.ok) {
    mostrarMensaje(resultado.error || "No se pudo guardar.", "error");
    return;
  }

  form.reset();
  mostrarMensaje("Producto guardado en la base de datos.", "ok");
  await cargarProductos();
});

cargarProductos();
