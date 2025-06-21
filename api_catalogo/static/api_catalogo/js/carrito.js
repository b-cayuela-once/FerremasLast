document.addEventListener('DOMContentLoaded', async () => {
  let carrito = [];
  let carritoBloqueado = false;
  let despachoActivado = false;
  let pedidoAprobado = false;
  let pedidoRechazado = false;

  const contenedor = document.getElementById('carrito-contenido');
  const btnPago = document.getElementById('pago-btn');

  async function obtenerCarrito() {
    try {
      const response = await fetch('/api/venta/obtener_carrito/', {
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      });
      const data = await response.json();

      carrito = data.productos || [];
      carritoBloqueado = data.bloqueado || false;
      despachoActivado = data.despacho || false;

      pedidoAprobado = data.pedido_aprobado === true;
      pedidoRechazado = data.pedido_aprobado === false;

      renderCarrito();
      actualizarBotonPago();
    } catch (error) {
      console.error('Error al obtener carrito:', error);
      contenedor.innerHTML = '<p>Error al cargar el carrito.</p>';
    }
  }

  async function guardarCarrito() {
    try {
      await fetch('/api/venta/actualizar_carrito/', {
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
    } catch (error) {
      console.error('Error al guardar carrito:', error);
    }
  }

  function renderCarrito() {
    contenedor.innerHTML = '';
    if (carrito.length === 0) {
      contenedor.innerHTML = '<p class="mensaje-vacio">Tu carrito está vacío</p>';
      return;
    }

    let total = 0;
    carrito.forEach((p, index) => {
      const item = document.createElement('div');
      item.classList.add('producto-carrito');
      item.innerHTML = `
        <div class="info-producto">
          <img src="${p.imagen}" alt="${p.nombre}">
          <div class="detalle-producto">
            <span class="nombre">${p.nombre}</span>
            <span class="precio">$${p.precio}</span>
          </div>
        </div>
        <div class="cantidad-controles">
          <button class="btn-quitar" ${carritoBloqueado ? 'disabled' : ''} onclick="actualizarCantidad(${index}, -1)">➖</button>
          <span>${p.cantidad}</span>
          <button class="btn-agregar" ${carritoBloqueado ? 'disabled' : ''} onclick="actualizarCantidad(${index}, 1)">➕</button>
        </div>
      `;
      contenedor.appendChild(item);
      total += p.precio * p.cantidad;
    });

    const controlDespacho = document.createElement('div');
    controlDespacho.classList.add('control-despacho');
    controlDespacho.innerHTML = `
      <label>
        <input type="checkbox" id="toggle-despacho" ${despachoActivado ? 'checked' : ''} ${carritoBloqueado ? 'disabled' : ''}>
        Agregar despacho por $5.000
      </label>
    `;
    contenedor.appendChild(controlDespacho);

    // ✅ Aquí escuchamos cambios en el checkbox de despacho
    const toggle = document.getElementById('toggle-despacho');
    if (toggle) {
      toggle.addEventListener('change', async (e) => {
        despachoActivado = e.target.checked;
        await guardarCarrito();
        renderCarrito();
        actualizarBotonPago();
      });
    }

    const valorDespacho = despachoActivado ? 5000 : 0;
    const resumen = document.createElement('div');
    resumen.classList.add('total-carrito');
    resumen.innerHTML = `
      <p>Total sin despacho: <strong>$${total}</strong></p>
      <p>Total final: <strong>$${total + valorDespacho}</strong></p>
    `;
    contenedor.appendChild(resumen);

    if (carritoBloqueado && !pedidoAprobado) {
      const msg = document.createElement('p');
      msg.textContent = "🔒 El carrito ha sido bloqueado. Esperando confirmación de Ejecutivo...";
      msg.style.marginTop = '15px';
      msg.style.color = '#dc0c19';
      msg.style.fontWeight = 'bold';
      msg.style.textAlign = 'center';
      contenedor.appendChild(msg);
    } else if (pedidoAprobado) {
      const msg = document.createElement('p');
      msg.textContent = "✅ El carrito ha sido desbloqueado. Favor proceder a pagar";
      msg.style.marginTop = '15px';
      msg.style.color = '#28a745';
      msg.style.fontWeight = 'bold';
      msg.style.textAlign = 'center';
      contenedor.appendChild(msg);
    }
  }

  function actualizarBotonPago() {
    if (!btnPago) return;

    if (pedidoAprobado) {
      btnPago.disabled = false;
      btnPago.textContent = 'Proceder al pago';
      btnPago.onclick = () => {
        window.location.href = '/api/usuario/signup-form'; // 🔁 reemplaza por tu ruta real de pago
      };
    } else if (pedidoRechazado) {
      btnPago.disabled = false;
      btnPago.textContent = 'Pedido rechazado - Intenta enviar de nuevo';
      btnPago.onclick = async () => {
        btnPago.disabled = true;
        btnPago.textContent = 'Enviando pedido...';

        const total = carrito.reduce((acc, p) => acc + p.precio * p.cantidad, 0);
        const totalFinal = total + (despachoActivado ? 5000 : 0);

        try {
          const response = await fetch('/api/venta/crear_pedido/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
              productos: carrito,
              total: totalFinal,
              despacho: despachoActivado
            })
          });

          const result = await response.json();
          if (result.status === 'ok') {
            alert(`✅ Pedido #${result.pedido_id} creado. Total: $${totalFinal}`);
            carritoBloqueado = true;
            await guardarCarrito();
            renderCarrito();
            pedidoAprobado = false;
            pedidoRechazado = false;
            actualizarBotonPago();
          } else {
            alert('❌ Error al generar el pedido.');
            btnPago.disabled = false;
            btnPago.textContent = 'Pedido rechazado - Intenta enviar de nuevo';
          }
        } catch (err) {
          console.error(err);
          alert('⚠️ No se pudo conectar al servidor.');
          btnPago.disabled = false;
          btnPago.textContent = 'Pedido rechazado - Intenta enviar de nuevo';
        }
      };
    } else {
      btnPago.disabled = carritoBloqueado;
      btnPago.textContent = 'Proceder al pago';
      btnPago.onclick = async () => {
        if (carritoBloqueado) return;

        const total = carrito.reduce((acc, p) => acc + p.precio * p.cantidad, 0);
        const totalFinal = total + (despachoActivado ? 5000 : 0);

        try {
          const response = await fetch('/api/venta/crear_pedido/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
              productos: carrito,
              total: totalFinal,
              despacho: despachoActivado
            })
          });

          const result = await response.json();
          if (result.status === 'ok') {
            alert(`✅ Pedido #${result.pedido_id} creado. Total: $${totalFinal}`);
            carritoBloqueado = true;
            await guardarCarrito();
            renderCarrito();
            actualizarBotonPago();
          } else {
            alert('❌ Error al generar el pedido.');
          }
        } catch (err) {
          console.error(err);
          alert('⚠️ No se pudo conectar al servidor.');
        }
      };
    }
  }

  window.actualizarCantidad = async (index, cambio) => {
    if (carritoBloqueado) return;
    carrito[index].cantidad += cambio;
    if (carrito[index].cantidad < 1) {
      carrito.splice(index, 1);
    }
    await guardarCarrito();
    renderCarrito();
  };

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

  await obtenerCarrito();
});
