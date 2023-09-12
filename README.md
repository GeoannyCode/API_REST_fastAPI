# API REST FastAPI / Mongodb

Descripción corta del proyecto.

## Requisitos previos

Antes de comenzar, asegúrate de tener los siguientes requisitos:

- Python 3.7 o superior instalado.
- `virtualenv` instalado (para crear un entorno virtual).

## Configuración del Entorno de Desarrollo

1. Clona este repositorio en tu máquina local:

   ```shell
   $ git clone https://github.com/tuusuario/tuproyecto.git
   $ cd tuproyecto 
   ```

2. Crea un entorno virtual (venv). Si no tienes virtualenv instalado, puedes hacerlo con:

    ```shell
    $ pip install virtualenv
    ```

3. Crea un entorno virtual para tu proyecto:

    ```shell
    $ virtualenv venv
    ```
4. Activa el entorno virtual:
- En Linux/Mac:

    ```shell
    $ source venv/bin/activate
    ```
- En Windows (PowerShell):

    ```shell
    $ .\venv\Scripts\Activate
    ```
5. Instala las dependencias del proyecto desde el archivo requirements.txt:

    ```shell
    $ pip install -r requirements.txt
    ```

## Ejecución del Proyecto

Para ejecutar el proyecto, utiliza el siguiente comando:

    $ uvicorn app.main:app --reload
    
Esto iniciará el servidor FastAPI y podrás acceder a la aplicación en http://localhost:8000 en tu navegador.