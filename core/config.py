import os
from dotenv import load_dotenv

# --- Carga de Variables de Entorno ---
# La función `load_dotenv()` busca un archivo llamado `.env` en el directorio del proyecto
# y carga las variables definidas en él como si fueran variables de entorno del sistema.
# Esto es útil para mantener la configuración sensible (como claves secretas) fuera del código.
load_dotenv()

# --- Definición de Variables de Configuración ---
# Se leen las variables de entorno usando `os.getenv()`.
# El segundo argumento de `os.getenv()` es un valor por defecto que se usará si la variable no se encuentra.
# Esto es útil para que la aplicación pueda funcionar en desarrollo sin un archivo .env configurado.
SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))