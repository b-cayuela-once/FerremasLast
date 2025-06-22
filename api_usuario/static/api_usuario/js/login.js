// ===================================================
// 🔐 LOGIN GENERAL PARA USUARIOS (NO STAFF)
// ===================================================

// Escucha el evento 'submit' del formulario con ID 'login-form'
document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Previene el comportamiento por defecto (recarga de página)

    // -----------------------------------------------
    // 📝 Obtener datos del formulario
    // -----------------------------------------------
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
        // -----------------------------------------------
        // 📡 Enviar solicitud POST a la API para login
        // -----------------------------------------------
        const response = await fetch('/api/usuario/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Protección CSRF
            },
            body: JSON.stringify({ email, password }) // Enviar datos como JSON
        });

        const result = await response.json(); // Convertir respuesta en JSON
        const message = document.getElementById('message'); // Elemento para mostrar mensaje

        // ------------------------------------------------
        // ✅ Si las credenciales son correctas
        // ------------------------------------------------
        if (response.ok) {
            message.style.color = 'green';
            message.textContent = result.mensaje;

            // Redirige al catálogo después de 1.5 segundos
            setTimeout(() => {
                window.location.href = '/api/catalogo/catalogo/';
            }, 1500);

        } else {
            // ❌ Error en las credenciales o respuesta inválida
            message.style.color = 'red';
            message.textContent = result.error || "Error al iniciar sesión";
        }

    } catch (error) {
        // ⚠️ Error de red o fallo general
        console.error('Error en el login:', error);
        document.getElementById('message').textContent = "Error al conectar con el servidor.";
    }
});

// ===================================================
// 🍪 FUNCIÓN PARA OBTENER EL CSRF TOKEN DESDE LAS COOKIES
// ===================================================
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