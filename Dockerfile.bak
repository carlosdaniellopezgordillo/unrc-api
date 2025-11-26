# Railway Dockerfile - Backend only (FastAPI)
# Frontend se sirve desde React dev o se despliega en Vercel

FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Start command - usar shell para interpretar variable de entorno
CMD ["/bin/sh", "-c", "uvicorn unrc_api_main:app --host 0.0.0.0 --port ${PORT:-8000}"]
