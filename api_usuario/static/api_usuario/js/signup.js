// ===================================================
// ENVÍO DEL FORMULARIO DE REGISTRO DE USUARIO
// ===================================================

// Se ejecuta cuando se envía el formulario con ID 'signupForm'
document.getElementById('signupForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = e.target;
    // Se crea un objeto con los datos del formulario
    const data = {
        nombre: form.nombre.value,
        email: form.email.value,
        direccion: form.direccion.value,
        password: form.password.value
    };

    try {
        // Se envía la solicitud POST a la API de registro
        const response = await fetch('/api/usuario/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // importante para protección CSRF
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        const mensajeDiv = document.getElementById('mensaje');

        if (response.ok) {
            // Si el registro fue exitoso, muestra mensaje positivo y limpia el formulario
            mensajeDiv.style.color = 'green';
            mensajeDiv.innerText = result.mensaje;
            form.reset();

            // Después de mostrar el mensaje, redirigir al login-form después de 1.5 segundos
            setTimeout(() => {
                window.location.href = '/api/usuario/login-form';  // Ajusta esta URL a la ruta correcta de tu login
            }, 1500);
        } else {
            // Si ocurrió un error, muestra los mensajes de error en rojo
            mensajeDiv.style.color = 'red';
            mensajeDiv.innerText = Object.values(result).join('\n');
        }

    } catch (error) {
        // Si hay un error de conexión o servidor
        console.error('Error:', error);
        document.getElementById('mensaje').innerText = 'Error de conexión.';
    }
});

// Función para obtener el CSRF token de la cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmed = cookie.trim();
            // Busca la cookie con el nombre especificado
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
