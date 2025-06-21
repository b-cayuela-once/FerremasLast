# Imports.
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

# Maneja las peticiones del cliente, si el cliente solicita una petición que corresponda a "api_nombreapi", este revisara las URLS y esta URLS redireccionara a una vista en el VIEWS.PY.
urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye todas las URLS de la API_USUARIO.
    path('api/usuario/', include('api_usuario.urls')),
    # Incluye todas las URLS de la API_CATALOGO.
    path('api/catalogo/', include('api_catalogo.urls')),
    # Incluye la ruta base para el CATALOGO.
    path('', lambda request: HttpResponseRedirect('/api/catalogo/catalogo/')),
    # Incluye todas las URLS de la API_VENTA.
    path('api/venta/', include('api_venta.urls')),
]

# Esto sirve para mostrar imágenes en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)