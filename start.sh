#!/bin/bash
set -e
PORT=${PORT:-8000}
exec uvicorn unrc_api_main:app --host 0.0.0.0 --port "$PORT"
