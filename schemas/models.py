from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

# --- Enumeraciones (Enums) ---
class UserRole(str, Enum):
    estudiante = "estudiante"
    empresa = "empresa"
    administrador = "administrador"

class EstadoVinculacion(str, Enum):
    pendiente = "pendiente"
    en_proceso = "en_proceso"
    completado = "completado"
    rechazado = "rechazado"

# --- Modelos Base ---

class HabilidadBase(BaseModel):
    nombre: str

class ExperienciaBase(BaseModel):
    puesto: str
    empresa: str
    descripcion: str
    fecha_inicio: str
    fecha_fin: Optional[str] = None

class ProyectoBase(BaseModel):
    nombre: str
    descripcion: str
    url: Optional[str] = None

# --- Modelos para Creación (Create) ---

class HabilidadCreate(HabilidadBase):
    pass

class ExperienciaCreate(ExperienciaBase):
    pass

class ProyectoCreate(ProyectoBase):
    pass

# --- Modelos Completos con ID (para respuestas de API) ---

class Habilidad(HabilidadBase):
    id: int

    class Config:
        from_attributes = True

class Experiencia(ExperienciaBase):
    id: int

    class Config:
        from_attributes = True

class Proyecto(ProyectoBase):
    id: int

    class Config:
        from_attributes = True

# --- Modelos de Perfiles (Estudiante y Empresa) ---

class Estudiante(BaseModel):
    usuario_id: int
    matricula: str = Field(..., min_length=8, max_length=15)
    semestre: int = Field(..., ge=1, le=10)
    carrera: str
    gpa: float = Field(..., ge=0.0, le=4.0)
    habilidades_tecnicas: List[str] = []
    habilidades_blandas: List[str] = []
    proyectos: List[str] = []
    disponibilidad: bool = True
    experiencias: List[Experiencia] = []
    habilidades: List[Habilidad] = []

    class Config:
        from_attributes = True

class EstudianteConUsuario(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    matricula: str
    semestre: int
    carrera: str
    gpa: float
    habilidades_tecnicas: List[str] = []
    habilidades_blandas: List[str] = []
    proyectos: List[str] = []
    disponibilidad: bool = True
    usuario: Optional['User'] = None
    experiencias: List[Experiencia] = []
    habilidades: List[Habilidad] = []

    class Config:
        from_attributes = True

class Empresa(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    email_contacto: Optional[str] = None
    telefono: Optional[str] = None
    ubicacion: Optional[str] = None
    website: Optional[str] = None
    numero_empleados: Optional[str] = None

    class Config:
        from_attributes = True

class EmpresaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    email_contacto: Optional[str] = None
    telefono: Optional[str] = None
    ubicacion: Optional[str] = None
    website: Optional[str] = None
    numero_empleados: Optional[str] = None

# --- Modelos de Usuario ---

class UserBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str
    tipo: UserRole

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    tipo: Optional[UserRole] = None

class User(UserBase):
    id: int
    activo: bool = True
    fecha_creacion: datetime
    estudiante: Optional[Estudiante] = None

    class Config:
        from_attributes = True

# --- Modelos de Autenticación y Tokens ---

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserInfo(BaseModel):
    id: int
    nombre: str
    tipo: UserRole

class TokenWithUser(Token):
    user: UserInfo

# --- Modelos de Oportunidades y Vinculaciones ---

class Oportunidad(BaseModel):
    id: Optional[int] = None
    empresa_id: int
    titulo: str = Field(..., min_length=5, max_length=200)
    descripcion: str
    tipo: str = Field(..., pattern=r'^(practica|servicio_social|empleo)$')
    habilidades_requeridas: List[str] = []
    semestre_minimo: int = Field(..., ge=1, le=10)
    gpa_minimo: Optional[float] = Field(None, ge=0.0, le=10.0)
    ubicacion: str
    modalidad: str = Field(..., pattern=r'^(presencial|remoto|hibrido)$')
    duracion_meses: Optional[int] = None
    salario: Optional[float] = None
    fecha_publicacion: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
    activa: bool = True

    class Config:
        from_attributes = True

class Vinculacion(BaseModel):
    id: Optional[int] = None
    estudiante_id: int
    oportunidad_id: int
    puntuacion_compatibilidad: float = Field(..., ge=0.0, le=100.0)
    estado: EstadoVinculacion = EstadoVinculacion.pendiente
    fecha_vinculacion: Optional[datetime] = None
    comentarios: Optional[str] = None

class OportunidadCreate(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=200)
    descripcion: str
    tipo: str = Field(..., pattern=r'^(practica|servicio_social|empleo)$')
    habilidades_requeridas: List[str] = []
    semestre_minimo: int = Field(..., ge=1, le=10)
    gpa_minimo: Optional[float] = Field(None, ge=0.0, le=10.0)
    ubicacion: str
    modalidad: str = Field(..., pattern=r'^(presencial|remoto|hibrido)$')
    duracion_meses: Optional[int] = None
    salario: Optional[float] = None
    fecha_cierre: Optional[datetime] = None
    activa: bool = True

class OportunidadUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=5, max_length=200)
    descripcion: Optional[str] = None
    tipo: Optional[str] = Field(None, pattern=r'^(practica|servicio_social|empleo)$')
    habilidades_requeridas: Optional[List[str]] = None
    semestre_minimo: Optional[int] = Field(None, ge=1, le=10)
    gpa_minimo: Optional[float] = Field(None, ge=0.0, le=10.0)
    ubicacion: Optional[str] = None
    modalidad: Optional[str] = Field(None, pattern=r'^(presencial|remoto|hibrido)$')
    duracion_meses: Optional[int] = None
    salario: Optional[float] = None
    fecha_cierre: Optional[datetime] = None
    activa: Optional[bool] = None
