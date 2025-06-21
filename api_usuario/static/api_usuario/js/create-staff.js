// ===================================================
// ENVÍO DEL FORMULARIO PARA CREAR USUARIOS STAFF
// ===================================================

// Obtiene el evento "submit" del formulario con ID 'create-staff-form'.
document.getElementById('create-staff-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    // Obtiene los valores ingresados.
    const nombre = document.getElementById('nombre').value;
    const password = document.getElementById('password').value;
    const tipo_usuario = document.getElementById('tipo_usuario').value;
    const respuesta = document.getElementById('respuesta');

    try {
        // Envia una solicitud POST a la API para crear un nuevo usuario staff.
        const response = await fetch('/api/usuario/create-staff', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        // Convertir los datos del formulario a JSON.
            body: JSON.stringify({
                nombre,
                password,
                tipo_usuario
            })
        });

        // Convertir la respuesta en un objeto JSON.
        const data = await response.json();

        if (response.ok) {
            // Si la respuesta es exitosa (código 200–299), muestra mensaje positivo
            respuesta.textContent = data.mensaje;
            respuesta.style.color = 'green';
            document.getElementById('create-staff-form').reset();
        } else {
            // Si hay un error (por ejemplo, validación fallida), muestra el mensaje de error
            respuesta.textContent = data.error || 'Error al crear usuario';
            respuesta.style.color = 'red';
        }

    } catch (error) {
        // Si ocurre un error en la red o servidor, muestra mensaje de error genérico
        console.error(error);
        respuesta.textContent = 'Error de conexión con el servidor';
        respuesta.style.color = 'red';
    }
});

// Función para obtener el TOKEN CSRF desde las cookies
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + '=')) {
            return decodeURIComponent(trimmed.slice(name.length + 1));
        }
    }
    return '';
}