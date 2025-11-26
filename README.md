# 🎯 API Vinculación UNRC - Sistema Inteligente de Gestión del Talento

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue?logo=react&logoColor=white)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway)](https://railway.app)

## 📋 Descripción

**API Vinculación UNRC** es un sistema inteligente de gestión del talento humano desarrollado para la Universidad Nacional de Rosario Castellanos (UNRC). Utiliza algoritmos avanzados de matching basados en **TF-IDF** y **NLP** para conectar estudiantes con oportunidades laborales de manera automática.

### ✨ Características Principales

- 🔐 **Autenticación JWT**: Sistema seguro de autenticación sin estado
- 👨‍🎓 **Perfiles Inteligentes**: Gestión de perfiles de estudiantes y empresas
- 🎯 **Matching TF-IDF**: Algoritmo de compatibilidad semántica
- 📄 **Parseo de CV**: Extracción automática de datos con spaCy NLP
- 🤖 **Machine Learning**: Scoring inteligente de compatibilidad
- 📊 **API REST**: Documentación automática con Swagger/ReDoc
- 🔒 **Seguridad**: bcrypt, JWT, CORS configurado
- 🌐 **Frontend React**: Interfaz moderna y responsiva
- 📱 **Componentes Modulares**: Dashboard para estudiantes y empresas

---

## 🚀 Quick Start

### Requisitos Previos
- Python 3.9+
- Node.js 16+
- Git

### Instalación Local

#### 1️⃣ Clonar repositorio
```bash
git clone https://github.com/tuusuario/unrc-api.git
cd unrc-api
```

#### 2️⃣ Setup Backend
```bash
# Crear ambiente virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python unrc_api_main.py
```

Backend disponible en: `http://localhost:8000`

#### 3️⃣ Setup Frontend
```bash
cd frontend
npm install
npm start
```

Frontend disponible en: `http://localhost:3000`

---

## 📚 Documentación API

Una vez ejecutada la API, accede a:

| Documentación | URL |
|---|---|
| **Swagger UI** | `http://localhost:8000/docs` |
| **ReDoc** | `http://localhost:8000/redoc` |

### Endpoints Principales

#### 🔐 Autenticación
```http
POST   /auth/register           # Registrar usuario
POST   /auth/login              # Login
POST   /auth/verify-token       # Verificar JWT
```

#### 👨‍🎓 Estudiantes
```http
GET    /estudiantes             # Listar todos
GET    /estudiantes/{id}        # Obtener perfil
PUT    /estudiantes/{id}        # Actualizar perfil
POST   /estudiantes/{id}/upload-cv  # Cargar CV
```

#### 🏢 Empresas
```http
GET    /empresas                # Listar todas
GET    /empresas/{id}           # Obtener perfil
PUT    /empresas/{id}           # Actualizar perfil
```

#### 💼 Oportunidades (⭐ PUNTO CLAVE)
```http
GET    /oportunidades                     # Listar todas
GET    /oportunidades/recomendadas/{id}   # ⭐ Matching Inteligente
POST   /oportunidades                     # Crear oferta
PUT    /oportunidades/{id}                # Editar oferta
DELETE /oportunidades/{id}                # Eliminar oferta
```

---

## 🏗️ Arquitectura del Proyecto

```
unrc-api/
├── 📄 unrc_api_main.py         # Punto de entrada FastAPI
├── 📋 requirements.txt         # Dependencias Python
├── 🌐 frontend/                # React App
│   ├── src/
│   │   ├── components/         # Componentes React
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── 🛣️ routers/                 # Endpoints API
│   ├── auth.py
│   ├── estudiantes.py
│   ├── empresas.py
│   ├── oportunidades.py
│   ├── habilidades.py
│   ├── experiencias.py
│   └── proyectos.py
├── ⚙️ services/                # Lógica de negocio
│   ├── cv_parser.py            # Parseo de CV con spaCy
│   └── matching.py             # Algoritmo TF-IDF
├── 🔒 security/                # Autenticación
│   └── core.py                 # JWT + bcrypt
├── 🗄️ db/                      # Base de datos
│   └── database.py
├── 🏗️ schemas/                 # Modelos
│   └── models.py               # SQLAlchemy ORM
├── ⚙️ core/                    # Configuración
│   └── config.py
├── 📁 uploaded_cvs/            # CVs subidos
├── 📄 .env                     # Variables de entorno
├── 🐳 Dockerfile               # Containerización
├── 🚂 railway.toml             # Config Railway
└── 📖 README.md                # Este archivo
```

---

## 🚂 Deployment en Railway

### 1️⃣ Requisitos
- Cuenta GitHub
- Cuenta Railway (gratuita)
- Repositorio público

### 2️⃣ Conectar GitHub a Railway

```bash
# 1. Crear repositorio en GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tuusuario/unrc-api.git
git push -u origin main
```

### 3️⃣ Deploy en Railway

1. Ve a https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Selecciona el repositorio
4. Railway detecta automáticamente Python + Node.js
5. Click "Deploy" ✅

### 4️⃣ Configurar Variables de Entorno

En Railway Dashboard:
- Variables → Add Variable
- Agregar:
  ```
  DATABASE_URL = postgresql://...
  SECRET_KEY = tu_llave_super_secreta
  PYTHON_VERSION = 3.9
  NODE_ENV = production
  ```

### 5️⃣ URLs de Railway

```
Backend:   https://tu-proyecto.up.railway.app
Frontend:  https://tu-proyecto-web.up.railway.app (si está configurado)
```

---

## 📖 Ejemplos de Uso

### Registrar Estudiante
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "estudiante@unrc.edu.mx",
    "password": "securepass123",
    "full_name": "Carlos López",
    "role": "estudiante"
  }'
```

### Cargar CV
```bash
curl -X POST "http://localhost:8000/estudiantes/1/upload-cv" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@cv.pdf"
```

### Obtener Recomendaciones
```bash
curl -X GET "http://localhost:8000/oportunidades/recomendadas/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🧠 Tecnologías Utilizadas

### Backend
| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **FastAPI** | 0.100+ | Framework web async |
| **Uvicorn** | Latest | Servidor ASGI |
| **SQLAlchemy** | Latest | ORM para BD |
| **Pydantic** | Latest | Validación de datos |
| **PyJWT** | Latest | Tokens JWT |
| **Passlib + bcrypt** | Latest | Seguridad contraseñas |

### AI/ML
| Tecnología | Propósito |
|-----------|----------|
| **spaCy** (es_core_news_sm) | NLP - CV Parsing |
| **scikit-learn** | TF-IDF - Similarity |

### Frontend
| Tecnología | Versión |
|-----------|---------|
| **React** | 18+ |
| **React Router** | v6 |
| **axios** | Latest |

### Bases de Datos
| Tecnología | Ambiente |
|-----------|----------|
| **SQLite** | Desarrollo |
| **PostgreSQL** | Producción (Railway) |

---

## 🔄 Flujo Principal: Matching de Oportunidades

```
1. Estudiante abre Dashboard
   ↓
2. Frontend obtiene estudianteId de localStorage
   ↓
3. React hace GET /oportunidades/recomendadas/{id}
   ↓
4. Backend:
   a) Obtiene datos del estudiante
   b) Obtiene todas las oportunidades
   c) Para CADA oportunidad:
      • Llama matching.calcular_compatibilidad()
      • Recibe score 0-100
   d) Ordena por score DESC
   e) Filtra score > 30
   f) Retorna array ordenado
   ↓
5. React renderiza oportunidades
   ↓
6. Estudiante ve ofertas RANKED por compatibilidad ✅
```

### 🎯 Algoritmo de Matching (TF-IDF)

**Criterios ponderados:**
- ✓ Semestre: 20%
- ✓ GPA: 15%
- ✓ Habilidades (TF-IDF): 40%
- ✓ Experiencia: 15%
- ✓ Proyectos: 10%
- ✓ Disponibilidad: 5%

**Rango final: 0-100**

---

## 🔒 Seguridad

- ✅ **Contraseñas**: Hash bcrypt (no plain text)
- ✅ **Tokens**: JWT con expiración
- ✅ **CORS**: Configurado para production
- ✅ **SQL Injection**: SQLAlchemy ORM + Pydantic
- ✅ **HTTPS**: Automático en Railway
- ✅ **Validación**: Pydantic en todos los endpoints

---

## 📊 Modelo de Base de Datos

```
user (Principal)
├── id, email (UNIQUE), hashed_password, full_name, role
└── 1-a-1
    ├─→ estudiante (semestre, gpa, carrera, disponibilidad)
    │   └─ 1-a-N → habilidad, experiencia, proyecto
    └─→ empresa (nombre, descripcion, industria)
        └─ 1-a-N → oportunidad (requisitos, score)
```

---

## 🧪 Testing

```bash
pytest tests/
pytest --cov=. tests/
pytest tests/test_auth.py -v
```

---

## 📝 Variables de Entorno (.env)

```env
DATABASE_URL=sqlite:///./database.db
SECRET_KEY=tu_llave_super_larga
ALGORITHM=HS256
CORS_ORIGINS=["http://localhost:3000"]
SPACY_MODEL=es_core_news_sm
```

---

## 🎓 Aprendizajes Clave

Este proyecto demuestra:

1. **Backend profesional**: FastAPI modular
2. **Autenticación**: JWT + bcrypt
3. **ML**: TF-IDF + NLP con spaCy
4. **Frontend**: React moderno
5. **DevOps**: CI/CD con Railway
6. **Databases**: SQLAlchemy ORM
7. **API REST**: RESTful + Swagger
8. **Seguridad**: Best practices

---

## 📜 Licencia

Proyecto académico - UNRC 2024-2025

---

## 👥 Autores

- **Carlos Daniel Lopez Gordillo** - Backend + ML
- **Andrea Monserrat Hernandez De la Cruz** - Frontend + UX

**8º Semestre** - Licenciatura en Ciencia de Datos para Negocios
**Universidad Nacional de Rosario Castellanos (UNRC)**

---

## 🌟 Status

- ✅ Backend: Production Ready
- ✅ Frontend: Production Ready
- ✅ Matching: Tested
- ✅ CV Parser: v2.0
- 🚀 Ready for Railway Deployment

**Última actualización**: Noviembre 2024