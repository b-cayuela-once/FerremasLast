// ===================================================
// 📝 REGISTRO DE USUARIO - FORMULARIO DE SIGNUP
// ===================================================

// ===================================================
// Evento de envío del formulario de registro
// ===================================================

// Escucha el evento 'submit' del formulario con ID 'signupForm'
document.getElementById('signupForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // Previene la recarga de la página al enviar el formulario

    const form = e.target;

    // ---------------------------------------------------
    // 📦 Obtener los datos ingresados en el formulario
    // ---------------------------------------------------
    const data = {
        nombre: form.nombre.value,
        email: form.email.value,
        direccion: form.direccion.value,
        password: form.password.value
    };

    try {
        // ---------------------------------------------------
        // 📡 Enviar solicitud POST a la API de registro
        // ---------------------------------------------------
        const response = await fetch('/api/usuario/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Protección contra ataques CSRF
            },
            body: JSON.stringify(data) // Datos del formulario en formato JSON
        });

        const result = await response.json(); // Convertir respuesta en JSON
        const mensajeDiv = document.getElementById('mensaje');

        // ---------------------------------------------------
        // ✅ Registro exitoso
        // ---------------------------------------------------
        if (response.ok) {
            mensajeDiv.style.color = 'green';
            mensajeDiv.innerText = result.mensaje;
            form.reset(); // Limpia el formulario

            // Redirige al formulario de login después de 1.5 segundos
            setTimeout(() => {
                window.location.href = '/api/usuario/login-form'; // Ajusta la ruta si es necesario
            }, 1500);

        } else {
            // ---------------------------------------------------
            // ❌ Error en el registro (por validaciones del backend)
            // ---------------------------------------------------
            mensajeDiv.style.color = 'red';
            mensajeDiv.innerText = Object.values(result).join('\n'); // Muestra todos los errores
        }

    } catch (error) {
        // ---------------------------------------------------
        // ⚠️ Error de red o del servidor
        // ---------------------------------------------------
        console.error('Error:', error);
        document.getElementById('mensaje').innerText = 'Error de conexión.';
    }
});

// ===================================================
// 🍪 FUNCIÓN PARA OBTENER EL TOKEN CSRF DESDE LAS COOKIES
// ===================================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmed = cookie.trim();
            // Verifica si la cookie actual es la que buscamos
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}