#!/bin/bash
# Script para iniciar la aplicación con variables de entorno
PORT=${PORT:-8000}
exec uvicorn unrc_api_main:app --host 0.0.0.0 --port $PORT
