// ===================================================
// 🎯 ENVÍO DEL FORMULARIO PARA CREAR USUARIOS STAFF
// ===================================================

// Al enviar el formulario con ID 'create-staff-form'
document.getElementById('create-staff-form').addEventListener('submit', async function (e) {
    e.preventDefault();  // Evita recarga de página por defecto

    // -----------------------------------------------
    // 📝 RECOLECCIÓN DE DATOS DEL FORMULARIO
    // -----------------------------------------------
    const nombre = document.getElementById('nombre').value;
    const password = document.getElementById('password').value;
    const tipo_usuario = document.getElementById('tipo_usuario').value;
    const respuesta = document.getElementById('respuesta');

    try {
        // -----------------------------------------------
        // 📡 ENVÍO DE DATOS A LA API PARA CREAR STAFF
        // -----------------------------------------------
        const response = await fetch('/api/usuario/create-staff', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), // Incluye token CSRF para seguridad
            },
            body: JSON.stringify({
                nombre,
                password,
                tipo_usuario
            })
        });

        const data = await response.json(); // Parsea la respuesta como JSON

        // -----------------------------------------------
        // ✅ RESPUESTA EXITOSA
        // -----------------------------------------------
        if (response.ok) {
            respuesta.textContent = data.mensaje;
            respuesta.style.color = 'green';
            document.getElementById('create-staff-form').reset(); // Limpia formulario
        } 
        // -----------------------------------------------
        // ❌ ERROR EN LA RESPUESTA (VALIDACIÓN U OTRO)
        // -----------------------------------------------
        else {
            respuesta.textContent = data.error || 'Error al crear usuario';
            respuesta.style.color = 'red';
        }

    } catch (error) {
        // -----------------------------------------------
        // ⚠️ ERROR DE CONEXIÓN O SERVIDOR
        // -----------------------------------------------
        console.error(error);
        respuesta.textContent = 'Error de conexión con el servidor';
        respuesta.style.color = 'red';
    }
});

// ===================================================
// 🔒 FUNCIÓN PARA OBTENER EL TOKEN CSRF DE LAS COOKIES
// ===================================================
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