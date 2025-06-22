// ===================================================
// 🔐 LOGIN PARA USUARIOS STAFF (Administrador, Vendedor, etc.)
// ===================================================

// Escucha el evento 'submit' del formulario con ID 'loginStaffForm'
document.getElementById('loginStaffForm').addEventListener('submit', async function (e) {
  e.preventDefault(); // Previene el comportamiento por defecto (recarga)

  // -----------------------------------------------
  // 📝 Obtener datos ingresados en el formulario
  // -----------------------------------------------
  const nombre = document.getElementById('nombre').value;
  const password = document.getElementById('password').value;

  try {
    // -----------------------------------------------
    // 📡 Enviar solicitud POST para autenticar al usuario staff
    // -----------------------------------------------
    const response = await fetch('/api/usuario/login-staff', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken() // Seguridad contra ataques CSRF
      },
      body: JSON.stringify({ nombre, password }) // Datos del formulario en formato JSON
    });

    const data = await response.json(); // Convertir respuesta en JSON
    const mensajeDiv = document.getElementById('mensaje'); // Elemento para mostrar mensajes

    // -------------------------------------------------------
    // ✅ Si la autenticación fue exitosa
    // -------------------------------------------------------
    if (response.ok) {
      // 🛑 Si el backend indica que el usuario debe cambiar su contraseña
      if (data.change_password_required) {
        mensajeDiv.textContent = "Debe cambiar su contraseña.";
        setTimeout(() => {
          window.location.href = '/api/usuario/forgot-password-staff-form'; // Redirección a formulario de cambio
        }, 1500);
      } else {
        // 🔓 Login exitoso sin cambio de contraseña obligatorio
        mensajeDiv.style.color = "green";
        mensajeDiv.textContent = "Login exitoso.";

        // ---------------------------------------------------
        // 🔁 Redirección según el tipo de usuario staff
        // ---------------------------------------------------
        setTimeout(() => {
          const tipo = data.tipo_usuario?.toLowerCase(); // Asegura que esté en minúsculas

          if (tipo === 'administrador') {
            window.location.href = '/api/catalogo/admin_site/';
          } else if (tipo === 'vendedor') {
            window.location.href = '/api/venta/vendedor_site/';
          } else if (tipo === 'bodeguero') {
            window.location.href = '/api/venta/bodeguero_site/';
          } else if (tipo === 'contador') {
            window.location.href = '/api/venta/contador_site/';
          } else {
            // ❌ Tipo de usuario no válido
            mensajeDiv.style.color = "red";
            mensajeDiv.textContent = "Tipo de usuario no reconocido.";
          }
        }, 1500);
      }

    } else {
      // 🚫 Error de autenticación (credenciales incorrectas, etc.)
      mensajeDiv.textContent = data.error || "Error al iniciar sesión.";
    }

  } catch (error) {
    // ⚠️ Error en la conexión con el servidor o en el fetch
    console.error('Error:', error);
    document.getElementById('mensaje').textContent = "Error al conectar con el servidor.";
  }
});

// ===================================================
// 🔒 FUNCIÓN PARA OBTENER EL TOKEN CSRF DESDE LAS COOKIES
// ===================================================
function getCSRFToken() {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') return value;
  }
  return '';
}