// ===================================================
// 🔐 FORMULARIO PARA RESTABLECER CONTRASEÑA STAFF
// ===================================================

document.addEventListener('DOMContentLoaded', function () {
    // -----------------------------------------------
    // 📋 Referencias a elementos del DOM
    // -----------------------------------------------
    const form = document.getElementById('forgotPasswordForm');
    const mensaje = document.getElementById('mensaje');

    // ---------------------------------------------------
    // 📤 ENVÍO DEL FORMULARIO AL SERVIDOR AL HACER SUBMIT
    // ---------------------------------------------------
    form.addEventListener('submit', async function (e) {
        e.preventDefault(); // Evita recarga automática de la página

        // 📝 Obtener valores del formulario
        const nombre = document.getElementById('nombre').value;
        const nueva_password = document.getElementById('nueva_password').value;

        try {
            // 📡 Enviar solicitud POST al backend
            const response = await fetch('/api/usuario/forgot-password-staff', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Protección CSRF
                },
                body: JSON.stringify({ nombre, nueva_password })
            });

            const data = await response.json(); // Procesa la respuesta JSON

            // ✅ Si la solicitud fue exitosa
            if (response.ok) {
                mensaje.style.color = 'green';
                mensaje.textContent = data.mensaje;

                // ⏳ Redirige a login luego de un pequeño delay
                setTimeout(() => {
                    window.location.href = '/api/usuario/login-form-staff';
                }, 1500);
            } 
            // ❌ Si hubo un error desde el backend
            else {
                mensaje.style.color = 'red';
                mensaje.textContent = data.error || 'Ocurrió un error';
            }

        } catch (error) {
            // ⚠️ Si ocurre un error de conexión o inesperado
            console.error('Error:', error);
            mensaje.style.color = 'red';
            mensaje.textContent = 'Error de conexión con el servidor';
        }
    });

    // ===================================================
    // 🔒 FUNCIÓN PARA OBTENER EL TOKEN CSRF DE LAS COOKIES
    // ===================================================
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