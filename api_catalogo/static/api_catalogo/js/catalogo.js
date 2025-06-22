// =======================================================
// 🛍️ CATÁLOGO DE PRODUCTOS - CLIENTE
// Script para mostrar productos, cambiar cantidades y 
// agregar al carrito con control de bloqueo.
// =======================================================

// =========================
// 🔧 Variables globales
// =========================
let carrito = [];                 // Productos actuales en el carrito
let carritoBloqueado = false;     // Si el carrito está bloqueado
let despachoActivado = false;     // Si se activó despacho
let cantidades = {};              // Cantidades seleccionadas por producto

// =========================
// 📦 Cargar productos del catálogo y mostrarlos
// =========================
fetch('/api/catalogo/api/')
  .then(response => response.json())
  .then(productos => {
    const contenedor = document.getElementById('productos');

    productos.forEach(p => {
      const card = document.createElement('div');
      card.className = 'producto';
      card.innerHTML = `
        <img src="${p.imagen}" alt="${p.nombre}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 6px;">
        <h3>${p.nombre}</h3>
        <p>${p.descripcion}</p>
        <strong>$${p.precio}</strong>
        <div style="margin: 10px 0;">
          <button onclick="cambiarCantidad('${p.id}', -1)">➖</button>
          <span id="cantidad-${p.id}">1</span>
          <button onclick="cambiarCantidad('${p.id}', 1)">➕</button>
        </div>
        <button onclick="agregarAlCarrito('${p.id}', '${p.nombre}', ${p.precio}, '${p.imagen}')">Agregar al carrito</button>
      `;
      contenedor.appendChild(card);
    });
  })
  .catch(error => {
    console.error('Error cargando productos:', error);
  });

// =========================
// 🛒 Obtener carrito del backend al iniciar
// =========================
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('/api/venta/obtener_carrito/', {
      method: 'GET',
      headers: { 'X-CSRFToken': getCookie('csrftoken') }
    });
    const data = await response.json();
    carrito = data.productos || [];
    carritoBloqueado = data.bloqueado || false;
    despachoActivado = data.despacho || false;
  } catch (error) {
    console.error('Error al cargar carrito:', error);
  }
});

// =========================
// ➕➖ Cambiar cantidad seleccionada de un producto
// =========================
function cambiarCantidad(id, cambio) {
  if (!(id in cantidades)) cantidades[id] = 1;
  cantidades[id] += cambio;
  if (cantidades[id] < 1) cantidades[id] = 1;

  const span = document.getElementById(`cantidad-${id}`);
  if (span) span.textContent = cantidades[id];
}

// =========================
// 🧺 Agregar producto al carrito (con validación)
// =========================
async function agregarAlCarrito(id, nombre, precio, imagen) {
  if (carritoBloqueado) {
    alert("🔒 El carrito está bloqueado. No puedes agregar productos.");
    return;
  }

  const cantidad = cantidades[id] || 1;

  // Verificar si el producto ya está en el carrito
  const existente = carrito.find(p => p.id === id);
  if (existente) {
    existente.cantidad += cantidad;
  } else {
    carrito.push({ id, nombre, precio, imagen, cantidad });
  }

  try {
    const res = await fetch('/api/venta/actualizar_carrito/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        productos: carrito,
        despacho: despachoActivado,
        bloqueado: carritoBloqueado
      })
    });

    // Verificar si la petición fue exitosa
    if (!res.ok) {
      if (res.status === 403) {
        throw new Error("⚠️ Debes iniciar sesión para agregar productos al carrito.");
      } else {
        throw new Error("❌ Error desconocido al guardar el carrito.");
      }
    }

    const resultado = await res.json();
    if (resultado.status === 'ok') {
      alert(`${cantidad} unidad(es) de "${nombre}" agregado(s) al carrito.`);
      cantidades[id] = 1;
      const span = document.getElementById(`cantidad-${id}`);
      if (span) span.textContent = 1;
    } else {
      alert("❌ Error al guardar el carrito.");
    }
  } catch (err) {
    console.error('Error al guardar en backend:', err);
    alert(err.message);
  }
}

// =========================
// 🍪 Obtener valor de cookie CSRF
// =========================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
