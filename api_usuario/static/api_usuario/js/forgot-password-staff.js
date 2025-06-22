// ===================================================
// ENVÍO DEL FORMULARIO PARA RESTABLECER CONTRASEÑA STAFF
// ===================================================

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('forgotPasswordForm');
    const mensaje = document.getElementById('mensaje');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value;
        const nueva_password = document.getElementById('nueva_password').value;

        const response = await fetch('/api/usuario/forgot-password-staff', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ nombre, nueva_password })
        });

        const data = await response.json();

        if (response.ok) {
            mensaje.style.color = 'green';
            mensaje.textContent = data.mensaje;

            setTimeout(() => {
                window.location.href = '/api/usuario/login-form-staff';
            }, 1500);
        } else {
            mensaje.style.color = 'red';
            mensaje.textContent = data.error || 'Ocurrió un error';
        }
    });

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
