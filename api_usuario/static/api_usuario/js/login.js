// ===================================================
// ENVÍO DEL FORMULARIO DE LOGIN GENERAL
// ===================================================

// Obtiene el evento 'submit' del formulario con ID 'login-form'
document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    // Obtiene los valores del formulario
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    // Envía una solicitud POST a la API de login
    const response = await fetch('/api/usuario/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ email, password })
    });

    // Convierte la respuesta a un objeto JSON
    const result = await response.json();
    const message = document.getElementById('message');

    if (response.ok) {
        // Si el login fue exitoso
        message.style.color = 'green';
        message.textContent = result.mensaje;

        // Después de mostrar el mensaje, redirigir al login-form después de 1.5 segundos
        setTimeout(() => {
            window.location.href = '/api/catalogo/catalogo/';  // Ajusta esta URL a la ruta correcta de tu login
        }, 1500);
    } else {
        // Si hubo un error de autenticación
        message.style.color = 'red';
        message.textContent = result.error || "Error al iniciar sesión";
    }
});

// Función para obtener el CSRF token de la cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            const cookie = c.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}