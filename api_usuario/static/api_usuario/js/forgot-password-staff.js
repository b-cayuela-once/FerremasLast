// ===================================================
// ENVÍO DEL FORMULARIO PARA RESTABLECER CONTRASEÑA STAFF
// ===================================================

document.addEventListener('DOMContentLoaded', function () {
    // Obtiene el formulario y el elemento donde se mostrará el mensaje
    const form = document.getElementById('forgotPasswordForm');
    const mensaje = document.getElementById('mensaje');

    // Escucha el evento 'submit' del formulario
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Obtiene los valores ingresados por el usuario
        const nombre = document.getElementById('nombre').value;
        const nueva_password = document.getElementById('nueva_password').value;

        // Realiza la solicitud POST a la API para restablecer la contraseña
        const response = await fetch('/api/usuario/forgot-password-staff', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ nombre, nueva_password })
        });

        // Convierte la respuesta en objeto JSON
        const data = await response.json();
        if (response.ok) {
            // Si la respuesta fue exitosa, muestra el mensaje y redirige
            mensaje.style.color = 'green';
            mensaje.textContent = data.mensaje;
            setTimeout(() => {
                window.location.href = '/api/usuario/welcome-staff';
            }, 1500); // espera 1.5 segundos antes de redirigir
        } else {
            // Si hubo un error, muestra mensaje correspondiente
            mensaje.style.color = 'red';
            mensaje.textContent = data.error || 'Ocurrió un error';
        }
    });

// Función para obtener el TOKEN CSRF desde las cookies
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
});
