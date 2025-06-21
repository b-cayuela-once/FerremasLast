// ===================================================
// ENVÍO DEL FORMULARIO DE LOGIN PARA USUARIOS STAFF
// ===================================================

// Obtiene el evento 'submit' del formulario con ID 'loginStaffForm'
document.getElementById('loginStaffForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  // Obtiene los valores ingresados por el usuario
  const nombre = document.getElementById('nombre').value;
  const password = document.getElementById('password').value;

  try {
    // Realiza una solicitud POST a la API para iniciar sesión
    const response = await fetch('/api/usuario/login-staff', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      // Datos del formulario en formato JSON
      body: JSON.stringify({ nombre, password })
    });

    // Convierte la respuesta del servidor en un objeto JSON
    const data = await response.json();
    const mensajeDiv = document.getElementById('mensaje');

    if (response.ok) {
      // Si el servidor indica que debe cambiar su contraseña
      if (data.change_password_required) {
        mensajeDiv.textContent = "Debe cambiar su contraseña.";
        setTimeout(() => {
          window.location.href = '/api/usuario/forgot-password-staff-form';
        }, 1500); // espera 1.5 segundos antes de redirigir
      } else {
        // Si el login fue exitoso y no requiere cambiar contraseña
        mensajeDiv.style.color = "green";
        mensajeDiv.textContent = "Login exitoso.";

        // ========================================
        // ✅ Redirección según tipo de usuario
        // ========================================
        setTimeout(() => {
          const tipo = data.tipo_usuario?.toLowerCase(); // Asegura que esté en minúsculas
          
          if (tipo === 'administrador' || tipo === 'contador') {
            window.location.href = '/api/catalogo/admin_site/';
          } else if (tipo === 'vendedor' || tipo === 'bodeguero') {
            window.location.href = '/api/catalogo/lista/';
          } else {
            mensajeDiv.style.color = "red";
            mensajeDiv.textContent = "Tipo de usuario no reconocido.";
          }
        }, 1500);
      }
    } else {
      // Si la autenticación falla, muestra el mensaje de error devuelto por la API
      mensajeDiv.textContent = data.error || "Error al iniciar sesión.";
    }

  } catch (error) {
    // Si ocurre un error de red o del servidor, lo muestra por consola y al usuario
    console.error('Error:', error);
    document.getElementById('mensaje').textContent = "Error al conectar con el servidor.";
  }
});

// ===================================================
// FUNCIÓN PARA OBTENER EL CSRF TOKEN DESDE LAS COOKIES
// ===================================================
function getCSRFToken() {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') return value;
  }
  return '';
}
