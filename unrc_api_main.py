from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import HTMLResponse, FileResponse
import logging
import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Descargar modelo spaCy en startup (solo si no existe)
try:
    import spacy
    spacy.load("es_core_news_sm")
except OSError:
    logger_temp = logging.getLogger(__name__)
    logger_temp.info("Descargando modelo spaCy es_core_news_sm...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "es_core_news_sm"])

# Se importa el router de autenticación. A medida que crees más routers, los importarás aquí.
from routers import auth, habilidades, experiencias, proyectos, empresas, oportunidades, estudiantes

# --- 2. Configuración del Logging ---
# Configura un sistema básico de logging para registrar eventos importantes de la aplicación.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 3. Creación de la Aplicación FastAPI ---
# Se crea la instancia principal de la aplicación FastAPI.
app = FastAPI(
    title="API Vinculación UNRC",
    description="API inteligente para la gestión del talento humano de la UNRC",
    version="1.0.0"
)

# --- 4. Configuración de Middleware (CORS) ---
# Cross-Origin Resource Sharing (CORS) permite que un frontend (ej. una app web en otro dominio)
# pueda hacer peticiones a esta API. Es una medida de seguridad del navegador.

# Lista de orígenes permitidos en producción
origins = [
    "http://localhost:3000", # Para desarrollo con React
    # "https://tu-dominio-de-produccion.com", # Agrega aquí tu dominio de producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Usar la lista de orígenes
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"], # Especificar métodos
    allow_headers=["Authorization", "Content-Type"], # Especificar cabeceras
)

# --- 5. Inclusión de Routers ---
# Aquí se "conectan" los endpoints definidos en otros archivos (como auth.py) a la aplicación principal.
# Cada router agrupa un conjunto de rutas relacionadas (ej. todo lo de autenticación).
app.include_router(auth.router)
app.include_router(habilidades.router)
app.include_router(experiencias.router)
app.include_router(proyectos.router)
app.include_router(empresas.router)
app.include_router(oportunidades.router)
app.include_router(estudiantes.router)


# --- 6. Endpoint Raíz (sirve index.html) ---
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Sirve la página principal estilizada."""
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    return FileResponse(index_path, media_type="text/html")

# --- 7. Ejecución de la Aplicación ---
# Este bloque permite ejecutar la API directamente con `python unrc_api_main.py`.
# uvicorn es el servidor ASGI que corre la aplicación FastAPI. `reload=False` desactiva el reinicio automático.
if __name__ == "__main__":
    uvicorn.run("unrc_api_main:app", host="0.0.0.0", port=8000, reload=False)