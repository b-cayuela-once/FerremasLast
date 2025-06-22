# APIS.

API_CATALOGO

API_USUARIO

API_VENTA

# PREPARAR DIRECTORIO.
(Antes de clonar el repositorio)

    PASO 1.- Crear carpeta.
    Crear carpeta *

    PASO 2.- Crear entorno virtual:
    python -m venv env

    PASO 3.- Activar entorno virtual:
    PASO 3.1.- Windows:
    .\env\Scripts\activate

    PASO 3.2.- macOS/Linux:
    source env/bin/activate

# CLONAR REPOSITORIO.
(Dentro de la carpeta creada, no dentro del entorno virtual)

    PASO 1.- Configurar Git:
    git config --global user.name "Tu Nombre"
    git config --global user.email "tunombre@ejemplo.com"

    PASO 2.- Clonar repositorio:
    git clone https://github.com/b-cayuela-once/proyecto0.git

# PREPARAR ENTORNO DE TRABAJO.

    PASO 1.- Instalar requirements.txt:
    pip install -r requirements.txt

    PASO 2.- Actualizar Pip en caso de ser necesario:
    python.exe -m pip install --upgrade pip

    PASO 3.- Realizar migraciones:
    python manage.py makemigrations

    PASO 4.- Migrar:
    python manage.py migrate

    PASO 5.- Crear SuperUsuario:
    python manage.py createsuperuser

# PREPARAR GIT PARA SUBIR CAMBIOS.

    PASO 1.- Establecer git en tu proyecto base:
    git init 

    PASO 2.- Establecer repositorio:
    git remote add origin https://github.com/b-cayuela-once/proyecto0.git

    PASO 3.- En caso de instalar mas bibliotecas:
    pip freeze > requirements.txt

    PASO 4.- Agregar todos los cambios:
    git add .

    PASO 5.- Commitear:
    git commit -m "Nombre del commit"

    PASO 6.- Subir al repositorio:
    git push -u origin main

# ALGUNOS COMANDOS DE DJANGO.

    * Arrancar servidor:
    python manage.py runserver

    * Crear Aplicación:
    python manage.py startapp "nombre app"

    * Crear superusuario:
    python manage.py createsuperuser

# TARGETAS.

    * Crédito: 4051 8856 0044 6623
    CVV:123
    Clave:123
    Rut:11.111.111-1
    Expiración: cualquiera en el futuro ej:12/29

    * Débito: 4051 8842 3993 7763
    Clave:123
    Rut:11.111.111-1